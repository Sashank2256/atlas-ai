import logging

from sqlalchemy.orm import Session

from app.crud.message import create_message, list_messages
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


class ChatService:
    def send_message(
        self,
        db: Session,
        conversation_id: int,
        content: str,
    ):
        logger.info(
            "Saving user message for conversation %s",
            conversation_id,
        )

        # Save user's message
        create_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=content,
        )

        logger.info(
            "Loading message history for conversation %s",
            conversation_id,
        )

        # Load full conversation history
        messages = list_messages(
            db=db,
            conversation_id=conversation_id,
        )

        # Convert to Ollama format
        ollama_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

        logger.info(
            "Sending conversation %s to LLM",
            conversation_id,
        )

        # Generate AI response
        assistant_reply = llm_service.chat(
            ollama_messages
        )

        logger.info(
            "LLM response received for conversation %s",
            conversation_id,
        )

        # Save assistant message
        assistant_message = create_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_reply,
        )

        logger.info(
            "Assistant response saved for conversation %s",
            conversation_id,
        )

        return assistant_message


chat_service = ChatService()