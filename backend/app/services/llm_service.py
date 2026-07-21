import ollama

from app.core.config import settings


class LLMService:
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


llm_service = LLMService()
