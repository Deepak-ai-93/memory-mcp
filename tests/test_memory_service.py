from sqlalchemy.orm import sessionmaker

from openmemory_mcp.memory.embeddings import HashEmbeddingProvider
from openmemory_mcp.models import MemoryType
from openmemory_mcp.services import MemoryService
from openmemory_mcp.storage import build_engine, init_database
from openmemory_mcp.storage.repositories import (
    SQLAlchemyDecisionRepository,
    SQLAlchemyMemoryRepository,
    SQLAlchemyProjectRepository,
)


def build_test_service(tmp_path):
    engine = build_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_database(engine)
    sessions = sessionmaker(engine)
    return MemoryService(
        projects=SQLAlchemyProjectRepository(sessions),
        memories=SQLAlchemyMemoryRepository(sessions),
        decisions=SQLAlchemyDecisionRepository(sessions),
        embeddings=HashEmbeddingProvider(),
    )


def test_remember_and_search_memory(tmp_path):
    service = build_test_service(tmp_path)

    result = service.remember(
        "demo", "The API is implemented in Python with FastMCP.", MemoryType.architecture, ["api"]
    )
    assert result["status"] == "stored"

    matches = service.search_memory("demo", "FastMCP Python", limit=5)["matches"]
    assert len(matches) == 1
    assert matches[0]["type"] == "architecture"


def test_add_and_get_decisions(tmp_path):
    service = build_test_service(tmp_path)

    result = service.add_decision("demo", "Use SQLite for local mode.", "It works offline.")
    assert "decision_id" in result

    decisions = service.get_decisions("demo")["decisions"]
    assert decisions[0]["decision"] == "Use SQLite for local mode."


def test_project_context_and_timeline(tmp_path):
    service = build_test_service(tmp_path)
    service.remember("demo", "Requirement: support PostgreSQL.", MemoryType.requirement, ["db"])
    service.remember("demo", "Prefer pytest for tests.", MemoryType.preference, ["tests"])
    service.add_decision("demo", "Use SQLAlchemy repositories.", "Keeps storage pluggable.")

    context = service.project_context("demo")
    assert context["project"] == "demo"
    assert context["requirements"]
    assert context["decisions"]
    assert context["standards"]

    events = service.timeline("demo")["events"]
    assert len(events) >= 3
