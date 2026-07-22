from sqlalchemy.orm import Session

from app.db.models import Message


def create_message(
    db: Session,
    *,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    """Create a message."""

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def list_messages(
    db: Session,
    *,
    conversation_id: int,
) -> list[Message]:
    """Return all messages in a conversation."""

    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
