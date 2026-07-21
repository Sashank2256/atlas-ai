from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Atlas AI"
    VERSION: str = "0.1.0"

    MODEL_NAME: str = "qwen2.5-coder:7b"
    OLLAMA_HOST: str = "http://localhost:11434"

    DEBUG: bool = True

    model_config = {
        "env_file": ".env",
    }


settings = Settings()
