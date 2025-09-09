"""Persistent conversation storage for μ-MCP."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ConversationStorage:
    """Handles persistent storage of multi-model conversations."""
    
    def __init__(self):
        """Initialize storage with default directory."""
        # Always use default ~/.mu-mcp/conversations
        self.storage_dir = Path.home() / ".mu-mcp" / "conversations"
        
        # Create directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache for conversations (no limit within MCP lifecycle)
        self._cache = {}
        
        # Track last conversation for "continue" command
        self._last_conversation_id = None
        self._last_model_used = None
        
        logger.info(f"Conversation storage initialized at: {self.storage_dir}")
    
    def save_conversation(self, conversation_id: str, messages: list, 
                         model_metadata: Optional[dict] = None) -> bool:
        """
        Save a conversation to disk and update cache.
        
        Args:
            conversation_id: Unique conversation identifier
            messages: List of message dicts with role and content
            model_metadata: Optional metadata about models used
        
        Returns:
            True if saved successfully
        """
        try:
            file_path = self.storage_dir / f"{conversation_id}.json"
            
            # Check if conversation exists to determine created time
            if file_path.exists():
                with open(file_path, "r") as f:
                    existing = json.load(f)
                    created = existing.get("created")
            else:
                created = datetime.utcnow().isoformat()
            
            # Prepare conversation data
            conversation_data = {
                "id": conversation_id,
                "created": created,
                "updated": datetime.utcnow().isoformat(),
                "messages": messages,
            }
            
            # Add model metadata if provided
            if model_metadata:
                conversation_data["model_metadata"] = model_metadata
            
            # Write to file
            with open(file_path, "w") as f:
                json.dump(conversation_data, f, indent=2)
            
            # Update cache (write-through)
            self._cache[conversation_id] = conversation_data
            
            # Update last conversation tracking
            self._last_conversation_id = conversation_id
            # Extract the last model used from messages or metadata
            if model_metadata and "models_used" in model_metadata:
                self._last_model_used = model_metadata["models_used"][-1] if model_metadata["models_used"] else None
            else:
                # Try to extract from the last assistant message
                for msg in reversed(messages):
                    if msg.get("role") == "assistant":
                        metadata = msg.get("metadata", {})
                        if "model" in metadata:
                            self._last_model_used = metadata["model"]
                            break
            
            logger.debug(f"Saved conversation {conversation_id} with {len(messages)} messages")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save conversation {conversation_id}: {e}")
            return False
    
    def load_conversation(self, conversation_id: str) -> Optional[dict]:
        """
        Load a conversation from cache or disk.
        
        Args:
            conversation_id: Unique conversation identifier
        
        Returns:
            Conversation data dict or None if not found
        """
        # Check cache first
        if conversation_id in self._cache:
            data = self._cache[conversation_id]
            logger.debug(f"Loaded conversation {conversation_id} from cache with {len(data.get('messages', []))} messages")
            return data
        
        # Not in cache, try loading from disk
        try:
            file_path = self.storage_dir / f"{conversation_id}.json"
            
            if not file_path.exists():
                logger.debug(f"Conversation {conversation_id} not found")
                return None
            
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Add to cache for future access
            self._cache[conversation_id] = data
            
            logger.debug(f"Loaded conversation {conversation_id} from disk with {len(data.get('messages', []))} messages")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load conversation {conversation_id}: {e}")
            return None
    
    def get_last_conversation_info(self) -> tuple[Optional[str], Optional[str]]:
        """
        Get the last conversation ID and model used.
        
        Returns:
            Tuple of (conversation_id, model_used) or (None, None) if no conversations
        """
        return self._last_conversation_id, self._last_model_used
    
    
    def get_messages_for_api(self, messages: list) -> list:
        """
        Extract just role and content for API calls.
        Strips metadata that OpenRouter doesn't understand.
        
        Args:
            messages: List of message dicts potentially with metadata
        
        Returns:
            Clean list of messages for API
        """
        clean_messages = []
        
        for msg in messages:
            # Only include role and content for API
            clean_msg = {
                "role": msg.get("role"),
                "content": msg.get("content")
            }
            clean_messages.append(clean_msg)
        
        return clean_messages
    
    def add_metadata_to_message(self, message: dict, metadata: dict) -> dict:
        """
        Add metadata to a message for storage.
        
        Args:
            message: Basic message dict with role and content
            metadata: Metadata to add (timestamp, model, etc.)
        
        Returns:
            Message with metadata added
        """
        return {
            **message,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                **metadata
            }
        }