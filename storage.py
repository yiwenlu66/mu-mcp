"""Persistent conversation storage for μ-MCP."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from models import get_short_name

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
                         model_metadata: Optional[dict] = None, title: Optional[str] = None) -> bool:
        """
        Save a conversation to disk and update cache.
        
        Args:
            conversation_id: Unique conversation identifier
            messages: List of message dicts with role and content
            model_metadata: Optional metadata about models used
            title: Optional conversation title
        
        Returns:
            True if saved successfully
        """
        try:
            file_path = self.storage_dir / f"{conversation_id}.json"
            
            # Check if conversation exists to determine created time
            existing = {}
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
            
            # Add title if provided or preserve existing title
            if title:
                conversation_data["title"] = title
            elif "title" in existing:
                conversation_data["title"] = existing["title"]
            
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
            last_full_name = None
            if model_metadata and "models_used" in model_metadata:
                last_full_name = model_metadata["models_used"][-1] if model_metadata["models_used"] else None
            else:
                # Try to extract from the last assistant message
                for msg in reversed(messages):
                    if msg.get("role") == "assistant":
                        metadata = msg.get("metadata", {})
                        if "model" in metadata:
                            last_full_name = metadata["model"]
                            break
            
            # Convert to short name for agent interface
            if last_full_name:
                short_name = get_short_name(last_full_name)
                self._last_model_used = short_name if short_name else last_full_name
            else:
                self._last_model_used = None
            
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
    
    def list_recent_conversations(self, limit: int = 20) -> list[dict]:
        """
        List the most recently updated conversations.
        
        Args:
            limit: Maximum number of conversations to return
        
        Returns:
            List of conversation summaries sorted by update time (newest first)
        """
        conversations = []
        
        try:
            # Get all conversation files with their modification times
            files_with_mtime = []
            for file_path in self.storage_dir.glob("*.json"):
                try:
                    mtime = file_path.stat().st_mtime
                    files_with_mtime.append((mtime, file_path))
                except Exception as e:
                    logger.warning(f"Failed to stat file {file_path}: {e}")
                    continue
            
            # Sort by modification time (newest first) and take only the limit
            files_with_mtime.sort(key=lambda x: x[0], reverse=True)
            recent_files = files_with_mtime[:limit]
            
            # Now load only the recent files
            for _, file_path in recent_files:
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        
                        # Extract key information
                        conv_summary = {
                            "id": data.get("id"),
                            "title": data.get("title"),
                            "created": data.get("created"),
                            "updated": data.get("updated"),
                        }
                        
                        # Extract model used from messages or metadata
                        model_full_name = None
                        if "model_metadata" in data and "models_used" in data["model_metadata"]:
                            models = data["model_metadata"]["models_used"]
                            model_full_name = models[-1] if models else None
                        else:
                            # Try to extract from the last assistant message
                            for msg in reversed(data.get("messages", [])):
                                if msg.get("role") == "assistant":
                                    metadata = msg.get("metadata", {})
                                    if "model" in metadata:
                                        model_full_name = metadata["model"]
                                        break
                        
                        # Convert to short name for agent interface
                        if model_full_name:
                            short_name = get_short_name(model_full_name)
                            model_used = short_name if short_name else model_full_name
                        else:
                            model_used = None
                        
                        conv_summary["model_used"] = model_used
                        
                        # If no title exists (should not happen with new version)
                        # just use a placeholder
                        if not conv_summary["title"]:
                            conv_summary["title"] = "[Untitled conversation]"
                        
                        conversations.append(conv_summary)
                        
                except Exception as e:
                    logger.warning(f"Failed to read conversation file {file_path}: {e}")
                    continue
            
            # The files are already in order from the filesystem sorting
            # But we should still sort by the actual "updated" field in case of discrepancies
            conversations.sort(key=lambda x: x.get("updated", ""), reverse=True)
            
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to list recent conversations: {e}")
            return []