import json
import math
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, sessionmaker

from openmemory_mcp.models import DecisionRecord, MemoryRecord, MemoryType
from openmemory_mcp.storage.orm import DecisionORM, MemoryORM, ProjectORM


def _memory_record(row: MemoryORM, score: float | None = None) -> MemoryRecord:
    return MemoryRecord(
        id=UUID(row.id),
        project=row.project,
        content=row.content,
        type=MemoryType(row.type),
        tags=json.loads(row.tags_json),
        created_at=row.created_at,
        score=score,
    )


def _decision_record(row: DecisionORM) -> DecisionRecord:
    return DecisionRecord(
        id=UUID(row.id),
        project=row.project,
        decision=row.decision,
        reason=row.reason,
        created_at=row.created_at,
    )


def _cosine(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left)) or 1.0
    right_norm = math.sqrt(sum(b * b for b in right)) or 1.0
    return dot / (left_norm * right_norm)


class ProjectRepository(ABC):
    @abstractmethod
    def ensure(self, project: str) -> None:
        pass

    @abstractmethod
    def list_projects(self) -> list[str]:
        pass


class MemoryRepository(ABC):
    @abstractmethod
    def add(
        self,
        project: str,
        content: str,
        memory_type: MemoryType,
        tags: list[str],
        embedding: list[float],
    ) -> MemoryRecord:
        pass

    @abstractmethod
    def search(
        self, project: str, query: str, query_embedding: list[float], limit: int
    ) -> list[MemoryRecord]:
        pass

    @abstractmethod
    def by_project(
        self,
        project: str,
        memory_types: list[MemoryType] | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[MemoryRecord]:
        pass


class DecisionRepository(ABC):
    @abstractmethod
    def add(self, project: str, decision: str, reason: str) -> DecisionRecord:
        pass

    @abstractmethod
    def by_project(self, project: str, limit: int = 100) -> list[DecisionRecord]:
        pass


class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, sessions: sessionmaker[Session]) -> None:
        self.sessions = sessions

    def ensure(self, project: str) -> None:
        with self.sessions() as session:
            existing = session.scalar(select(ProjectORM).where(ProjectORM.name == project))
            if existing is None:
                session.add(ProjectORM(name=project))
                session.commit()

    def list_projects(self) -> list[str]:
        with self.sessions() as session:
            return list(session.scalars(select(ProjectORM.name).order_by(ProjectORM.name)))


class SQLAlchemyMemoryRepository(MemoryRepository):
    def __init__(self, sessions: sessionmaker[Session]) -> None:
        self.sessions = sessions

    def add(
        self,
        project: str,
        content: str,
        memory_type: MemoryType,
        tags: list[str],
        embedding: list[float],
    ) -> MemoryRecord:
        with self.sessions() as session:
            row = MemoryORM(
                project=project,
                content=content,
                type=memory_type.value,
                tags_json=json.dumps(tags),
                embedding_json=json.dumps(embedding),
            )
            session.add(row)
            session.commit()
            session.refresh(row)
            return _memory_record(row)

    def search(
        self, project: str, query: str, query_embedding: list[float], limit: int
    ) -> list[MemoryRecord]:
        terms = [term.lower() for term in query.split() if term]
        with self.sessions() as session:
            rows = list(
                session.scalars(
                    select(MemoryORM)
                    .where(MemoryORM.project == project)
                    .order_by(MemoryORM.created_at.desc())
                    .limit(500)
                )
            )

        ranked: list[tuple[float, MemoryORM]] = []
        for row in rows:
            haystack = f"{row.content} {row.tags_json} {row.type}".lower()
            keyword_score = sum(1 for term in terms if term in haystack) / max(len(terms), 1)
            semantic_score = _cosine(query_embedding, json.loads(row.embedding_json))
            score = (0.45 * keyword_score) + (0.55 * semantic_score)
            if score > 0 or not terms:
                ranked.append((score, row))

        ranked.sort(key=lambda item: (item[0], item[1].created_at), reverse=True)
        return [_memory_record(row, score=score) for score, row in ranked[:limit]]

    def by_project(
        self,
        project: str,
        memory_types: list[MemoryType] | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 100,
    ) -> list[MemoryRecord]:
        filters = [MemoryORM.project == project]
        if memory_types:
            filters.append(MemoryORM.type.in_([memory_type.value for memory_type in memory_types]))
        if start:
            filters.append(MemoryORM.created_at >= start)
        if end:
            filters.append(MemoryORM.created_at <= end)

        with self.sessions() as session:
            rows = session.scalars(
                select(MemoryORM).where(and_(*filters)).order_by(MemoryORM.created_at.desc()).limit(limit)
            )
            return [_memory_record(row) for row in rows]


class SQLAlchemyDecisionRepository(DecisionRepository):
    def __init__(self, sessions: sessionmaker[Session]) -> None:
        self.sessions = sessions

    def add(self, project: str, decision: str, reason: str) -> DecisionRecord:
        with self.sessions() as session:
            row = DecisionORM(project=project, decision=decision, reason=reason)
            session.add(row)
            session.commit()
            session.refresh(row)
            return _decision_record(row)

    def by_project(self, project: str, limit: int = 100) -> list[DecisionRecord]:
        with self.sessions() as session:
            rows = session.scalars(
                select(DecisionORM)
                .where(or_(DecisionORM.project == project, DecisionORM.project == "*"))
                .order_by(DecisionORM.created_at.desc())
                .limit(limit)
            )
            return [_decision_record(row) for row in rows]
