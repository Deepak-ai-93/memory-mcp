from datetime import datetime
from typing import Any

from openmemory_mcp.memory import EmbeddingProvider
from openmemory_mcp.models import MemoryType, ProjectContext, TimelineEvent
from openmemory_mcp.storage.repositories import (
    DecisionRepository,
    MemoryRepository,
    ProjectRepository,
)
from openmemory_mcp.utils.validation import normalize_project, normalize_tags


class MemoryService:
    def __init__(
        self,
        projects: ProjectRepository,
        memories: MemoryRepository,
        decisions: DecisionRepository,
        embeddings: EmbeddingProvider,
    ) -> None:
        self.projects = projects
        self.memories = memories
        self.decisions = decisions
        self.embeddings = embeddings

    def remember(
        self,
        project: str,
        content: str,
        memory_type: MemoryType | str = MemoryType.fact,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        project = normalize_project(project)
        content = content.strip()
        if not content:
            raise ValueError("content cannot be empty")
        memory_type = MemoryType(memory_type)
        self.projects.ensure(project)
        record = self.memories.add(
            project,
            content,
            memory_type,
            normalize_tags(tags),
            self.embeddings.embed(content),
        )
        return {"memory_id": str(record.id), "status": "stored"}

    def search_memory(self, project: str, query: str, limit: int = 10) -> dict[str, Any]:
        project = normalize_project(project)
        query = query.strip()
        if not query:
            raise ValueError("query cannot be empty")
        records = self.memories.search(
            project,
            query,
            self.embeddings.embed(query),
            max(1, min(limit, 50)),
        )
        return {"matches": [record.model_dump(mode="json") for record in records]}

    def add_decision(self, project: str, decision: str, reason: str) -> dict[str, str]:
        project = normalize_project(project)
        decision = decision.strip()
        reason = reason.strip()
        if not decision or not reason:
            raise ValueError("decision and reason cannot be empty")
        self.projects.ensure(project)
        record = self.decisions.add(project, decision, reason)
        self.remember(project, decision, MemoryType.decision, ["decision"])
        return {"decision_id": str(record.id)}

    def get_decisions(self, project: str) -> dict[str, Any]:
        project = normalize_project(project)
        records = self.decisions.by_project(project)
        return {"decisions": [record.model_dump(mode="json") for record in records]}

    def project_context(self, project: str) -> dict[str, Any]:
        project = normalize_project(project)
        requirements = self.memories.by_project(project, [MemoryType.requirement], limit=25)
        standards = self.memories.by_project(
            project,
            [MemoryType.preference, MemoryType.architecture],
            limit=25,
        )
        stack = self.memories.search(
            project,
            "technology stack framework language database",
            [],
            10,
        )
        context = ProjectContext(
            project=project,
            stack=[memory.content for memory in stack],
            requirements=requirements,
            decisions=self.decisions.by_project(project, limit=25),
            standards=standards,
        )
        return context.model_dump(mode="json")

    def timeline(
        self,
        project: str,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        project = normalize_project(project)
        memories = self.memories.by_project(project, start=start, end=end, limit=limit)
        decisions = self.decisions.by_project(project, limit=limit)
        events = [
            TimelineEvent(
                id=memory.id,
                project=memory.project,
                kind=f"memory:{memory.type.value}",
                content=memory.content,
                created_at=memory.created_at,
                metadata={"tags": memory.tags},
            )
            for memory in memories
        ]
        events.extend(
            TimelineEvent(
                id=decision.id,
                project=decision.project,
                kind="decision",
                content=decision.decision,
                created_at=decision.created_at,
                metadata={"reason": decision.reason},
            )
            for decision in decisions
            if (start is None or decision.created_at >= start)
            and (end is None or decision.created_at <= end)
        )
        events.sort(key=lambda event: event.created_at)
        return {"events": [event.model_dump(mode="json") for event in events[:limit]]}
