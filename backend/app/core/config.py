from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Atlas AI"
    VERSION: str = "0.1.0"

    DEBUG: bool = False

    MODEL_NAME: str = "qwen2.5-coder:7b"
    OLLAMA_HOST: str = "http://localhost:11434"

    DATABASE_URL: str

    SECRET_KEY: str = Field(min_length=32)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        gt=0,
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        gt=0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()