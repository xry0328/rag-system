from __future__ import annotations

from src.domain.chat.value_objects import AgentEvent


def status_event(message: str) -> AgentEvent:
    return AgentEvent(type="status", payload={"message": message})

