"""Chat handler for μ-MCP."""

import base64
import logging
import mimetypes
import os
import uuid
from pathlib import Path
from typing import Optional, Union

import aiohttp

from models import (
    get_allowed_models,
    resolve_model,
    get_short_name,
)
from prompts import (
    get_llm_system_prompt,
    get_response_wrapper,
    get_request_wrapper,
)
from storage import ConversationStorage

logger = logging.getLogger(__name__)


class ChatHandler:
    """Handle chat interactions with OpenRouter models."""

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Initialize persistent storage with default directory
        self.storage = ConversationStorage()

    async def chat(
        self,
        prompt: str,
        model: str,  # Now required
        title: Optional[str] = None,
        continuation_id: Optional[str] = None,
        files: Optional[list[str]] = None,
        images: Optional[list[str]] = None,
        reasoning_effort: Optional[str] = "medium",
    ) -> dict:
        """
        Chat with an AI model.
        
        Args:
            prompt: The user's message
            model: Model name (required)
            title: Title for a new conversation (provide this OR continuation_id, not both)
            continuation_id: UUID to continue existing conversation (provide this OR title, not both)
            files: List of file paths to include
            images: List of image paths to include
            reasoning_effort: Reasoning depth - "low", "medium", or "high" (for models that support it)
        
        Returns dict with:
        - content: The model's response with wrapper
        - continuation_id: UUID for continuing this conversation
        - model_used: The actual model that was used
        """
        # Resolve model name/alias
        resolved_model = resolve_model(model)
        if not resolved_model:
            # If not found in registry, use as-is (might be full path)
            resolved_model = model
        
        # Validate: exactly one of title or continuation_id must be provided
        if (title and continuation_id):
            return {
                "error": "Cannot provide both 'title' and 'continuation_id'. Use 'title' for new conversations or 'continuation_id' to continue existing ones.",
                "continuation_id": None,
                "model_used": None,
            }
        
        if (not title and not continuation_id):
            return {
                "error": "Must provide either 'title' for a new conversation or 'continuation_id' to continue an existing one.",
                "continuation_id": None,
                "model_used": None,
            }
        
        # Get or create conversation
        messages_with_metadata = []
        if continuation_id:
            # Try to load from persistent storage
            conversation_data = self.storage.load_conversation(continuation_id)
            if conversation_data:
                messages_with_metadata = conversation_data.get("messages", [])
            else:
                # Fail fast - conversation not found
                return {
                    "error": f"Conversation {continuation_id} not found. Please start a new conversation or use a valid continuation_id.",
                    "continuation_id": None,
                    "model_used": None,
                }
        else:
            # New conversation with title provided
            continuation_id = str(uuid.uuid4())

        # Build the user message with metadata and request wrapper
        wrapped_prompt = prompt + get_request_wrapper()
        user_content = self._build_user_content(wrapped_prompt, files, images)
        user_message = self.storage.add_metadata_to_message(
            {"role": "user", "content": user_content},
            {"target_model": resolved_model}
        )
        messages_with_metadata.append(user_message)
        
        # Get clean messages for API (without metadata)
        api_messages = self.storage.get_messages_for_api(messages_with_metadata)
        
        # Add system prompt for the LLM
        system_prompt = get_llm_system_prompt(resolved_model)
        api_messages.insert(0, {"role": "system", "content": system_prompt})

        # Make API call
        response_text = await self._call_openrouter(
            api_messages, resolved_model, reasoning_effort
        )

        # Add assistant response with metadata
        assistant_message = self.storage.add_metadata_to_message(
            {"role": "assistant", "content": response_text},
            {"model": resolved_model, "model_used": resolved_model}
        )
        messages_with_metadata.append(assistant_message)
        
        # Save conversation to persistent storage
        # Pass title only for new conversations (when title was provided)
        self.storage.save_conversation(
            continuation_id,
            messages_with_metadata,
            {"models_used": [resolved_model]},
            title=title  # Will be None for continuations, actual title for new conversations
        )
        
        # Get short name for agent interface
        short_name = get_short_name(resolved_model)
        # Fall back to resolved model if not in registry (custom path)
        display_name = short_name if short_name else resolved_model
        
        # Add response wrapper for Claude with model identification
        wrapped_response = response_text + get_response_wrapper(display_name)

        return {
            "content": wrapped_response,
            "continuation_id": continuation_id,
            "model_used": display_name,
        }

    def _build_user_content(
        self, prompt: str, files: Optional[list[str]], images: Optional[list[str]]
    ) -> str | list:
        """Build user message content with files and images."""
        content_parts = []

        # Add main prompt
        content_parts.append({"type": "text", "text": prompt})

        # Add files as text
        if files:
            file_content = self._read_files(files)
            if file_content:
                content_parts.append({"type": "text", "text": f"\n\nFiles:\n{file_content}"})

        # Add images as base64 with proper MIME type
        if images:
            for image_path in images:
                result = self._encode_image(image_path)
                if result:
                    encoded_data, mime_type = result
                    content_parts.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{encoded_data}"},
                        }
                    )

        # If only text, return string; otherwise return multi-part content
        if len(content_parts) == 1:
            return prompt
        return content_parts

    def _read_files(self, file_paths: list[str]) -> str:
        """Read and combine file contents with token-based budgeting."""
        contents = []
        # Simple token estimation: ~4 chars per token
        # Reserve tokens for prompt and response
        max_file_tokens = 50_000  # ~200k chars
        total_tokens = 0

        for file_path in file_paths:
            try:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    content = path.read_text(errors="ignore")
                    # Estimate tokens
                    file_tokens = len(content) // 4
                    
                    if total_tokens + file_tokens > max_file_tokens:
                        # Truncate if needed
                        remaining_tokens = max_file_tokens - total_tokens
                        if remaining_tokens > 100:  # Worth including partial
                            char_limit = remaining_tokens * 4
                            content = content[:char_limit] + "\n[File truncated]"
                            contents.append(f"\n--- {file_path} ---\n{content}")
                        break
                    
                    contents.append(f"\n--- {file_path} ---\n{content}")
                    total_tokens += file_tokens
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")

        return "".join(contents)

    def _encode_image(self, image_path: str) -> Optional[tuple[str, str]]:
        """Encode image to base64 with proper MIME type."""
        try:
            path = Path(image_path)
            if path.exists() and path.is_file():
                # Detect MIME type
                mime_type, _ = mimetypes.guess_type(str(path))
                if not mime_type or not mime_type.startswith('image/'):
                    # Default to JPEG for unknown types
                    mime_type = 'image/jpeg'
                
                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                    return encoded, mime_type
        except Exception as e:
            logger.warning(f"Could not encode image {image_path}: {e}")
        return None

    async def _call_openrouter(
        self,
        messages: list,
        model: str,
        reasoning_effort: Optional[str],
    ) -> str:
        """Make API call to OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/mu-mcp",
            "X-Title": "μ-MCP Server",
        }

        data = {
            "model": model,
            "messages": messages,
        }

        # Add reasoning effort if specified
        # OpenRouter will automatically ignore this for non-reasoning models
        if reasoning_effort:
            data["reasoning"] = {
                "effort": reasoning_effort  # "low", "medium", or "high"
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenRouter API error: {response.status} - {error_text}")

                result = await response.json()
                return result["choices"][0]["message"]["content"]
