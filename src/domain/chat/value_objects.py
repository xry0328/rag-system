from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedContext:
    content: str
    score: float | None
    knowledge_base_id: str
    document_id: str
    chunk_id: str
    filename: str
    metadata: dict


@dataclass(frozen=True)
class AgentEvent:
    type: str
    payload: dict

