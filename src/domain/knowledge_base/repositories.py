from __future__ import annotations

from typing import Protocol

from src.domain.document.entities import Document
from src.domain.knowledge_base.entities import KnowledgeBase


class KnowledgeBaseRepository(Protocol):
    def create(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        ...

    def list(self) -> list[KnowledgeBase]:
        ...

    def get(self, knowledge_base_id: str) -> KnowledgeBase:
        ...

    def find_by_name(self, name: str) -> KnowledgeBase | None:
        ...

    def update(self, knowledge_base: KnowledgeBase) -> None:
        ...


class DocumentRepository(Protocol):
    def add(self, document: Document) -> Document:
        ...

    def update(self, document: Document) -> None:
        ...

    def list_by_knowledge_base(self, knowledge_base_id: str) -> list[Document]:
        ...

