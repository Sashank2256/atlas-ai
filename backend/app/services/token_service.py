from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.crud.refresh_token import (
    create_refresh_token as save_refresh_token,
)
from app.crud.refresh_token import (
    get_refresh_token,
    revoke_refresh_token,
)


def refresh_tokens(db: Session, refresh_token: str):
    """
    Validate a refresh token, revoke it,
    generate new access and refresh tokens,
    and store the new refresh token.
    """

    # Find refresh token in database
    db_token = get_refresh_token(db, refresh_token)

    if not db_token:
        return None

    # Check if revoked
    if db_token.revoked:
        return None

    # Check expiry
    if db_token.expires_at < datetime.now(timezone.utc):
        return None

    # Revoke old refresh token
    revoke_refresh_token(db, db_token)

    # Generate new access token
    access_token = create_access_token(
        data={
            "sub": db_token.user.username,
        }
    )

    # Generate new refresh token
    new_refresh_token = create_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(days=30)

    # Store new refresh token
    save_refresh_token(
        db=db,
        token=new_refresh_token,
        user_id=db_token.user.id,
        expires_at=expires_at,
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

def logout(db: Session, refresh_token: str) -> bool:
    """
    Logout a user by revoking the given refresh token.
    """

    # Find the refresh token
    db_token = get_refresh_token(db, refresh_token)

    # Token not found
    if not db_token:
        return False

    # Already revoked
    if db_token.revoked:
        return False

    # Revoke the token
    revoke_refresh_token(db, db_token)

    return True