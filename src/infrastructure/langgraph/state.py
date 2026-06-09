from __future__ import annotations

from typing import TypedDict

from src.domain.chat.value_objects import RetrievedContext


class AgentState(TypedDict):
    question: str
    knowledge_base_ids: list[str]
    top_k: int
    contexts: list[RetrievedContext]
    answer: str

