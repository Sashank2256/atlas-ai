from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.crud.refresh_token import create_refresh_token as save_refresh_token
from app.crud.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import (
    RefreshTokenRequest,
    Token,
    UserCreate,
    UserResponse,
)
from app.services.token_service import (
    logout,
    refresh_tokens,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return create_user(db, user)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and return access token and refresh token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return access token and refresh token.
    """

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
        }
    )

    refresh_token = create_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    save_refresh_token(
        db=db,
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a new access token and refresh token using a valid refresh token.
    """

    tokens = refresh_tokens(
        db=db,
        refresh_token=request.refresh_token,
    )

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired or revoked refresh token",
        )

    return Token(**tokens)

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
)
def logout_user(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Logout a user by revoking the refresh token.
    """

    success = logout(
        db=db,
        refresh_token=request.refresh_token,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or already revoked refresh token",
        )

    return {
        "message": "Successfully logged out"
    }

