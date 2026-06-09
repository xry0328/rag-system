from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.domain.document.entities import Document
from src.domain.knowledge_base.entities import KnowledgeBase
from src.domain.shared.exceptions import KnowledgeBaseNotFound


class JsonMetadataStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"knowledge_bases": [], "documents": []})

    def create(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        data = self._read()
        data["knowledge_bases"].append(asdict(knowledge_base))
        self._write(data)
        return knowledge_base

    def list(self) -> list[KnowledgeBase]:
        data = self._read()
        return [KnowledgeBase(**item) for item in data["knowledge_bases"]]

    def get(self, knowledge_base_id: str) -> KnowledgeBase:
        for knowledge_base in self.list():
            if knowledge_base.id == knowledge_base_id:
                return knowledge_base
        raise KnowledgeBaseNotFound(f"Knowledge base '{knowledge_base_id}' not found.")

    def find_by_name(self, name: str) -> KnowledgeBase | None:
        normalized = name.strip().casefold()
        for knowledge_base in self.list():
            if knowledge_base.name.casefold() == normalized:
                return knowledge_base
        return None

    def update(self, knowledge_base: KnowledgeBase) -> None:
        data = self._read()
        updated = False
        for index, item in enumerate(data["knowledge_bases"]):
            if item["id"] == knowledge_base.id:
                data["knowledge_bases"][index] = asdict(knowledge_base)
                updated = True
                break
        if not updated:
            raise KnowledgeBaseNotFound(f"Knowledge base '{knowledge_base.id}' not found.")
        self._write(data)

    def add(self, document: Document) -> Document:
        data = self._read()
        data["documents"].append(asdict(document))
        self._write(data)
        return document

    def update_document(self, document: Document) -> None:
        data = self._read()
        for index, item in enumerate(data["documents"]):
            if item["id"] == document.id:
                data["documents"][index] = asdict(document)
                self._write(data)
                return
        raise ValueError(f"Document '{document.id}' not found.")

    def list_by_knowledge_base(self, knowledge_base_id: str) -> list[Document]:
        data = self._read()
        return [
            Document(**item)
            for item in data["documents"]
            if item["knowledge_base_id"] == knowledge_base_id
        ]

    def _read(self) -> dict:
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, data: dict) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


class KnowledgeBaseJsonRepository:
    def __init__(self, store: JsonMetadataStore) -> None:
        self.store = store

    def create(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        return self.store.create(knowledge_base)

    def list(self) -> list[KnowledgeBase]:
        return self.store.list()

    def get(self, knowledge_base_id: str) -> KnowledgeBase:
        return self.store.get(knowledge_base_id)

    def find_by_name(self, name: str) -> KnowledgeBase | None:
        return self.store.find_by_name(name)

    def update(self, knowledge_base: KnowledgeBase) -> None:
        self.store.update(knowledge_base)


class DocumentJsonRepository:
    def __init__(self, store: JsonMetadataStore) -> None:
        self.store = store

    def add(self, document: Document) -> Document:
        return self.store.add(document)

    def update(self, document: Document) -> None:
        self.store.update_document(document)

    def list_by_knowledge_base(self, knowledge_base_id: str) -> list[Document]:
        return self.store.list_by_knowledge_base(knowledge_base_id)

