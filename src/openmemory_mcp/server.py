from datetime import datetime

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import JSONResponse

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


def build_auth_provider(settings: Settings) -> StaticTokenVerifier | None:
    api_keys = settings.api_keys
    if not api_keys:
        return None

    tokens = {
        key: {
            "client_id": settings.api_key_client_id,
            "scopes": ["memory:read", "memory:write"],
        }
        for key in api_keys
    }

    return StaticTokenVerifier(
        tokens=tokens,
        required_scopes=["memory:read"],
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
    mcp = FastMCP(settings.server_name, auth=build_auth_provider(settings))

    @mcp.custom_route("/", methods=["GET"])
    async def root(request: Request) -> JSONResponse:
        """Return public service information for browser visits."""
        base_url = str(request.base_url).rstrip("/")
        return JSONResponse(
            {
                "service": settings.server_name,
                "status": "running",
                "transport": settings.transport,
                "auth_required": bool(settings.api_keys),
                "mcp_endpoint": f"{base_url}{settings.http_path}",
                "health": f"{base_url}/health",
                "message": "Use the mcp_endpoint URL in an MCP client.",
            }
        )

    @mcp.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> JSONResponse:
        """Return a lightweight health check response."""
        return JSONResponse({"status": "healthy", "service": settings.server_name})

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

    if not settings.api_keys:
        print("WARNING: Running in HTTP mode without an API key. Your server is PUBLIC.")
        print("Set OPENMEMORY_API_KEY to secure your server.")

    mcp.run(
        transport=settings.transport,
        host=settings.http_host,
        port=settings.http_port,
        path=settings.http_path,
    )


if __name__ == "__main__":
    main()
