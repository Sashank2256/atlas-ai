from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(
    prefix="",
    tags=["Health"],
)


@router.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.VERSION,
        "model": settings.MODEL_NAME,
    }
