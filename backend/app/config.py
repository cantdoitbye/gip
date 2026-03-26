from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_infrastructure"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174,http://localhost:8000"
    environment: str = "development"
    app_name: str = "AI Infrastructure Planning System"
    debug: bool = True

    @property
    def cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
