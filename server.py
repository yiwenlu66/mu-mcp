#!/usr/bin/env python3
"""μ-MCP Server - Minimal MCP server for AI model interactions.

In contrast to zen-mcp's 10,000+ lines of orchestration,
μ-MCP provides pure model access with no hardcoded workflows.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from mcp import McpError, types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    TextContent,
    Tool,
    ServerCapabilities,
    ToolsCapability,
    Prompt,
    GetPromptResult,
    PromptMessage,
    PromptsCapability,
)

from models import get_allowed_models
from prompts import get_agent_tool_description

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Server("μ-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools - just one: chat."""
    # Build model enum for schema
    models = get_allowed_models()
    
    # Build model enum for schema
    model_enum = []
    model_descriptions = []
    
    for key, model in models.items():
        # Add the main model name
        model_enum.append(model.name)
        model_descriptions.append(f"• {model.name}: {model.description}")
    
    # Build the combined description
    models_description = "Select the AI model that best fits your task:\n\n" + "\n".join(model_descriptions)
    
    return [
        Tool(
            name="chat",
            description=get_agent_tool_description(),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Your message or question"
                    },
                    "model": {
                        "type": "string",
                        "enum": model_enum,
                        "description": models_description,
                    },
                    "continuation_id": {
                        "type": "string",
                        "description": "UUID from previous response to continue that conversation thread. Start fresh (omit this) when: switching topics, context too long, or keeping separate contexts per model",
                    },
                    "files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Absolute paths to files to include as context",
                    },
                    "images": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Absolute paths to images to include",
                    },
                    "reasoning_effort": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Reasoning depth for models that support it (low=20%, medium=50%, high=80% of computation)",
                        "default": "medium",
                    },
                },
                "required": ["prompt", "model"],  # Model is now required
            },
        )
    ]


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts for slash commands."""
    return [
        Prompt(
            name="chat",
            description="Start a chat with AI models",
            arguments=[],
        ),
        Prompt(
            name="continue",
            description="Continue the previous conversation",
            arguments=[],
        ),
        Prompt(
            name="challenge",
            description="Encourage critical thinking and avoid reflexive agreement",
            arguments=[],
        ),
        Prompt(
            name="discuss",
            description="Orchestrate multi-turn discussion among multiple AIs",
            arguments=[],
        ),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, Any] = None) -> GetPromptResult:
    """Generate prompt text for slash commands."""
    if name == "chat":
        return GetPromptResult(
            description="Start a chat with AI models",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="Use the chat tool to start a conversation with an AI model."
                    )
                )
            ],
        )
    elif name == "continue":
        # Get the latest conversation to provide continuation_id hint
        from chat_handler import ChatHandler
        handler = ChatHandler()
        continuation_id, model_used = handler.storage.get_last_conversation_info()
        
        if continuation_id:
            instruction_text = f"""Continue your previous conversation using the chat tool.

IMPORTANT: Use continuation_id: "{continuation_id}" to maintain conversation context.
Previous model used: {model_used if model_used else "unknown - select appropriate model"}

This allows you to access the full conversation history even if your context was compacted."""
        else:
            instruction_text = "No previous conversations found. Start a new conversation using the chat tool."
        
        return GetPromptResult(
            description="Continue the previous conversation",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=instruction_text
                    )
                )
            ],
        )
    elif name == "challenge":
        return GetPromptResult(
            description="Encourage critical thinking and avoid reflexive agreement",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="""CRITICAL REASSESSMENT MODE:

When using the chat tool, wrap your prompt with instructions for the AI to:
- Challenge ideas and think critically before responding
- Evaluate whether they actually agree or disagree
- Provide thoughtful analysis rather than reflexive agreement

Example: Instead of accepting a statement, ask the AI to examine it for accuracy, completeness, and reasoning flaws.
This promotes truth-seeking over compliance."""
                    )
                )
            ],
        )
    elif name == "discuss":
        return GetPromptResult(
            description="Orchestrate multi-turn discussion among multiple AIs",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="""MULTI-AI DISCUSSION MODE:

Use the chat tool to orchestrate a multi-turn discussion among diverse AI models.

Requirements:
1. Select models with complementary strengths based on the topic
2. Start fresh conversations (no continuation_id) for each model
3. Provide context about the topic and other participants' perspectives
4. Exchange key insights between models across multiple turns
5. Encourage constructive disagreement - not consensus for its own sake
6. Continue until either consensus emerges naturally OR sufficiently diverse perspectives are gathered

Do NOT stop after one round. Keep the discussion going through multiple exchanges until reaching a natural conclusion.
Synthesize findings, highlighting both agreements and valuable disagreements."""
                    )
                )
            ],
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls - just chat."""
    if name != "chat":
        raise McpError(f"Unknown tool: {name}")

    from chat_handler import ChatHandler

    try:
        handler = ChatHandler()
        result = await handler.chat(**arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        logger.error(f"Chat tool error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        logger.error("OPENROUTER_API_KEY environment variable not set")
        logger.error("Get your API key at: https://openrouter.ai/keys")
        sys.exit(1)

    # Log configuration
    models = get_allowed_models()
    logger.info(f"Starting μ-MCP Server...")
    logger.info(f"Available models: {len(models)}")
    
    # Use stdio transport
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="μ-mcp",
                server_version="2.0.0",
                capabilities=ServerCapabilities(
                    tools=ToolsCapability(),
                    prompts=PromptsCapability(),
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
