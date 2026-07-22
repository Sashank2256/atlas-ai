from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.crud.conversation import get_conversation
from app.crud.message import create_message, list_messages
from app.db.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import llm_service

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = get_conversation(
        db,
        request.conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    history = list_messages(
        db,
        conversation_id=request.conversation_id,
    )

    messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in history
    ]

    messages.append(
        {
            "role": "user",
            "content": request.message,
        }
    )

    create_message(
        db=db,
        conversation_id=request.conversation_id,
        role="user",
        content=request.message,
    )

    response = llm_service.chat(messages)

    create_message(
        db=db,
        conversation_id=request.conversation_id,
        role="assistant",
        content=response,
    )

    return ChatResponse(
        response=response,
    )
