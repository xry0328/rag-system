from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeBaseSummary:
    id: str
    name: str
    description: str
    document_count: int
    chunk_count: int
    updated_at: str

