from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Atlas AI"
    VERSION: str = "0.1.0"

    MODEL_NAME: str = "qwen2.5-coder:7b"
    OLLAMA_HOST: str = "http://localhost:11434"

    DATABASE_URL: str = "postgresql+psycopg://atlas:atlas@localhost:5432/atlas_ai"

    DEBUG: bool = True

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config = {
        "env_file": ".env",
    }


settings = Settings()
