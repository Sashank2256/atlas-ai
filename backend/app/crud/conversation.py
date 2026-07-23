from sqlalchemy.orm import Session

from app.db.models import Conversation


def create_conversation(
    db: Session,
    *,
    title: str,
    user_id: int,
) -> Conversation:
    """Create a new conversation."""

    conversation = Conversation(
        title=title,
        user_id=user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    """Return a conversation by ID."""

    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def list_conversations(
    db: Session,
    *,
    user_id: int,
) -> list[Conversation]:
    """Return all conversations for a user."""

    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

def update_conversation(
    db: Session,
    conversation: Conversation,
    *,
    title: str,
) -> Conversation:
    """Update a conversation."""

    conversation.title = title

    db.commit()
    db.refresh(conversation)

    return conversation


def delete_conversation(
    db: Session,
    conversation: Conversation,
) -> None:
    """Delete a conversation."""

    db.delete(conversation)
    db.commit()
