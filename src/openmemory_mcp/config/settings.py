import os
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
    api_key: str | None = Field(
        default=None,
        description="Optional bearer API key required for HTTP MCP requests.",
    )
    api_key_client_id: str = "openmemory-public-client"
    transport: Literal["stdio", "http", "streamable-http", "sse"] = Field(
        default_factory=lambda: "http" if os.environ.get("RENDER") == "true" else "stdio"
    )
    http_host: str = Field(
        default_factory=lambda: "0.0.0.0" if os.environ.get("RENDER") == "true" else "127.0.0.1"
    )
    http_port: int = Field(default_factory=lambda: int(os.environ.get("PORT", "8000")))
    http_path: str = "/mcp"


@lru_cache
def get_settings() -> Settings:
    return Settings()
