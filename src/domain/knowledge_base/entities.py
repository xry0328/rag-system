from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class KnowledgeBase:
    id: str
    name: str
    description: str = ""
    document_count: int = 0
    chunk_count: int = 0
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def rename(self, name: str) -> None:
        normalized = name.strip()
        if not normalized:
            raise ValueError("Knowledge base name cannot be empty.")
        self.name = normalized
        self.touch()

    def add_ingested_document(self, chunk_count: int) -> None:
        self.document_count += 1
        self.chunk_count += chunk_count
        self.touch()

    def touch(self) -> None:
        self.updated_at = utc_now()

