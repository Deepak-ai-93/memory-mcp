from datetime import datetime

from fastmcp import FastMCP
from sqlalchemy.orm import sessionmaker

from openmemory_mcp.config import Settings, get_settings
from openmemory_mcp.memory import build_embedding_provider
from openmemory_mcp.models import MemoryType
from openmemory_mcp.services import MemoryService
from openmemory_mcp.storage import build_engine, init_database
from openmemory_mcp.storage.repositories import (
    SQLAlchemyDecisionRepository,
    SQLAlchemyMemoryRepository,
    SQLAlchemyProjectRepository,
)


def build_service(settings: Settings | None = None) -> MemoryService:
    settings = settings or get_settings()
    engine = build_engine(settings.database_url)
    init_database(engine)
    sessions = sessionmaker(engine)
    return MemoryService(
        projects=SQLAlchemyProjectRepository(sessions),
        memories=SQLAlchemyMemoryRepository(sessions),
        decisions=SQLAlchemyDecisionRepository(sessions),
        embeddings=build_embedding_provider(settings),
    )


def create_mcp(service: MemoryService | None = None, settings: Settings | None = None) -> FastMCP:
    settings = settings or get_settings()
    service = service or build_service(settings)
    mcp = FastMCP(settings.server_name)

    @mcp.tool()
    def remember(
        project: str,
        content: str,
        type: MemoryType = MemoryType.fact,
        tags: list[str] | None = None,
    ) -> dict:
        """Store a project memory with type and optional tags."""
        return service.remember(project=project, content=content, memory_type=type, tags=tags)

    @mcp.tool()
    def search_memory(project: str, query: str, limit: int = settings.default_search_limit) -> dict:
        """Retrieve project memories using hybrid keyword and semantic search."""
        return service.search_memory(project=project, query=query, limit=limit)

    @mcp.tool()
    def add_decision(project: str, decision: str, reason: str) -> dict:
        """Store an architecture, product, or business decision and its rationale."""
        return service.add_decision(project=project, decision=decision, reason=reason)

    @mcp.tool()
    def get_decisions(project: str) -> dict:
        """Return decision history for a project."""
        return service.get_decisions(project=project)

    @mcp.tool()
    def project_context(project: str) -> dict:
        """Return a compact project summary."""
        return service.project_context(project=project)

    @mcp.tool()
    def timeline(
        project: str,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> dict:
        """Return chronological project memory and decision events."""
        return service.timeline(project=project, start=start, end=end, limit=limit)

    return mcp


mcp = create_mcp()


def main() -> None:
    settings = get_settings()
    if settings.transport == "stdio":
        mcp.run()
        return

    mcp.run(
        transport=settings.transport,
        host=settings.http_host,
        port=settings.http_port,
        path=settings.http_path,
    )


if __name__ == "__main__":
    main()
