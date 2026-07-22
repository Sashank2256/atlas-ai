from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.conversation import get_conversation
from app.crud.message import create_message, list_messages
from app.db.session import SessionLocal
from app.schemas import MessageCreate, MessageResponse

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=MessageResponse,
    status_code=201,
)
def create_message_endpoint(
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db,
        message.conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return create_message(
        db,
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
    )


@router.get(
    "/{conversation_id}",
    response_model=list[MessageResponse],
)
def list_messages_endpoint(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db,
        conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return list_messages(
        db,
        conversation_id=conversation_id,
    )
