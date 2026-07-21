import ollama

from app.core.config import settings


class AIService:
    def chat(self, message: str) -> str:
        response = ollama.chat(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return response["message"]["content"]


ai_service = AIService()
