import ollama

from app.core.config import settings


class LLMService:
    def chat(self, messages: list[dict]) -> str:
        response = ollama.chat(
            model=settings.MODEL_NAME,
            messages=messages,
        )

        return response["message"]["content"]


llm_service = LLMService()
