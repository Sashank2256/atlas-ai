from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.conversation import (
    create_conversation,
    delete_conversation,
    get_conversation,
    list_conversations,
)
from app.db.session import SessionLocal
from app.schemas import ConversationCreate, ConversationResponse

router = APIRouter(prefix="/conversations", tags=["Conversations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=201,
)
def create_conversation_endpoint(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(
        db,
        title=conversation.title,
        user_id=conversation.user_id,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
)
def list_conversations_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    return list_conversations(
        db,
        user_id=user_id,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation_endpoint(
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

    return conversation


@router.delete(
    "/{conversation_id}",
    status_code=204,
)
def delete_conversation_endpoint(
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

    delete_conversation(
        db,
        conversation,
    )
