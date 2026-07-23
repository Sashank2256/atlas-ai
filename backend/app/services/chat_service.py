from sqlalchemy.orm import Session

from app.crud.message import create_message, list_messages
from app.services.llm_service import llm_service


class ChatService:
    def send_message(
        self,
        db: Session,
        conversation_id: int,
        content: str,
    ):
        # Save user's message
        create_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=content,
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

        # Generate AI response
        assistant_reply = llm_service.chat(
            ollama_messages
        )

        # Save assistant message
        assistant_message = create_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_reply,
        )

        return assistant_message


chat_service = ChatService()