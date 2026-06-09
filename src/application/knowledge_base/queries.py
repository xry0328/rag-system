from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ListDocumentsQuery:
    knowledge_base_id: str

