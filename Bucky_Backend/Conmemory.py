import os
from datetime import datetime
from typing import List, Dict, Union
import logging
from mem0 import MemoryClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("memory")

class ConversationMemory:
    """Persistent conversation memory using Mem0"""

    def __init__(self, user_id: str, mem0_api_key: str = None):
        self.user_id = user_id

        api_key = mem0_api_key or os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY is required")

        self.memory_client = MemoryClient(api_key=api_key)
        logger.info(f"ConversationMemory initialized for user: {user_id}")

    def load_memory(self) -> List[Dict]:
        """Load memories safely (Mem0 now REQUIRES filters)"""
        try:
            memories = self.memory_client.get_all(
                user_id=self.user_id,
                filters={"user_id": self.user_id},
            )

            conversations = []
            for m in memories.get("results", []):
                conversations.append({
                    "memory_id": m.get("id"),
                    "memory_text": m.get("memory", ""),
                    "metadata": m.get("metadata", {}),
                })

            logger.info(f"Loaded {len(conversations)} memories for {self.user_id}")
            return conversations

        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return []

    def save_conversation(self, conversation) -> bool:
        """Save conversation safely (sync-safe, thread-safe)"""
        try:
            if hasattr(conversation, "model_dump"):
                conversation = conversation.model_dump()

            messages = []
            for msg in conversation.get("messages", []):
                if msg.get("type") != "message":
                    continue
                content = msg.get("content")
                if isinstance(content, list):
                    content = " ".join(map(str, content))
                if content:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": content.strip(),
                    })

            if not messages:
                return False

            self.memory_client.add(
                messages=messages,
                user_id=self.user_id,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "message_count": len(messages),
                },
            )

            logger.info("Conversation saved to Mem0")
            return True

        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return False
