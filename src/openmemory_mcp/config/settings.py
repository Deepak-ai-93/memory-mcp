from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="OPENMEMORY_", env_file=".env", extra="ignore")

    database_url: str = Field(
        default=f"sqlite:///{Path.home() / '.openmemory-mcp' / 'openmemory.db'}",
        description="SQLAlchemy database URL. Supports sqlite:/// and postgresql+psycopg://.",
    )
    embedding_provider: Literal["hash", "openai", "gemini", "sentence_transformers"] = "hash"
    embedding_model: str = "text-embedding-3-small"
    server_name: str = "OpenMemory MCP"
    default_search_limit: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
