from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Document:
    id: str
    knowledge_base_id: str
    filename: str
    source_path: str
    status: str = "processing"
    chunk_count: int = 0
    error: str = ""
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def mark_completed(self, chunk_count: int) -> None:
        self.status = "completed"
        self.chunk_count = chunk_count
        self.error = ""
        self.updated_at = utc_now()

    def mark_failed(self, error: str) -> None:
        self.status = "failed"
        self.error = error
        self.updated_at = utc_now()


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    knowledge_base_id: str
    document_id: str
    content: str
    metadata: dict

