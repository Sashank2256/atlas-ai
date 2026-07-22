from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken


def create_refresh_token(
    db: Session,
    token: str,
    user_id: int,
    expires_at: datetime,
):
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token


def get_refresh_token(
    db: Session,
    token: str,
):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    refresh_token.revoked = True
    db.commit()


def delete_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    db.delete(refresh_token)
    db.commit()

def revoke_all_user_tokens(
    db: Session,
    user_id: int,
):
    (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        )
        .update({"revoked": True})
    )

    db.commit()