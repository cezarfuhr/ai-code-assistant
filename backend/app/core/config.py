"""
Configuration settings for the AI Code Assistant backend.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Code Assistant"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered code assistant for generation, explanation, and debugging"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
