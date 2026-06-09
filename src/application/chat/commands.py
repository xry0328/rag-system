from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatCommand:
    question: str
    knowledge_base_ids: list[str]
    provider: str
    model: str | None = None
    temperature: float = 0.2
    top_k: int = 5

