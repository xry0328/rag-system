from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateKnowledgeBaseCommand:
    name: str
    description: str = ""


@dataclass(frozen=True)
class IngestMarkdownCommand:
    knowledge_base_id: str
    filename: str
    content: bytes

