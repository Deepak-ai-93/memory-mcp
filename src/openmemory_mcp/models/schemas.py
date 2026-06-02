from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MemoryType(str, Enum):
    fact = "fact"
    decision = "decision"
    requirement = "requirement"
    task = "task"
    issue = "issue"
    meeting = "meeting"
    architecture = "architecture"
    preference = "preference"


class MemoryRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project: str
    content: str
    type: MemoryType
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    score: float | None = None


class DecisionRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project: str
    decision: str
    reason: str
    created_at: datetime


class TimelineEvent(BaseModel):
    id: UUID
    project: str
    kind: str
    content: str
    created_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProjectContext(BaseModel):
    project: str
    stack: list[str] = Field(default_factory=list)
    requirements: list[MemoryRecord] = Field(default_factory=list)
    decisions: list[DecisionRecord] = Field(default_factory=list)
    standards: list[MemoryRecord] = Field(default_factory=list)
