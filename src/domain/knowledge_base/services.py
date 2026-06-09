from __future__ import annotations

from src.domain.knowledge_base.entities import KnowledgeBase
from src.domain.shared.exceptions import KnowledgeBaseAlreadyExists


class KnowledgeBaseDomainService:
    def ensure_can_create(self, existing: KnowledgeBase | None, name: str) -> None:
        if not name.strip():
            raise ValueError("Knowledge base name cannot be empty.")
        if existing is not None:
            raise KnowledgeBaseAlreadyExists(f"Knowledge base '{name}' already exists.")

