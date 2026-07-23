import logging
import time

import ollama

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def chat(self, messages: list[dict]) -> str:
        logger.info(
            "Sending request to Ollama using model '%s'",
            settings.MODEL_NAME,
        )

        start = time.perf_counter()

        response = ollama.chat(
            model=settings.MODEL_NAME,
            messages=messages,
        )

        elapsed = time.perf_counter() - start

        logger.info(
            "LLM completed in %.2f seconds using model '%s'",
            elapsed,
            settings.MODEL_NAME,
        )

        return response["message"]["content"]


llm_service = LLMService()