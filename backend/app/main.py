from fastapi import FastAPI

from app.api.router import api_router
from app.api.v1.chat import router as chat_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.health import router as health_router
from app.api.v1.messages import router as messages_router
from app.core.config import settings
from app.core.middleware import log_requests

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Local AI assistant powered by Ollama and FastAPI.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.middleware("http")(log_requests)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(api_router)
app.include_router(
    conversations_router,
    prefix="/api/v1",
)

app.include_router(
    messages_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Atlas AI API",
        "docs": "/docs",
        "health": "/health",
    }
