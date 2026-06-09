from __future__ import annotations

from src.domain.chat.value_objects import RetrievedContext


class ChatDomainService:
    def build_context_block(self, contexts: list[RetrievedContext]) -> str:
        if not contexts:
            return "No relevant context was found."
        blocks = []
        for index, item in enumerate(contexts, start=1):
            source = item.filename or item.document_id
            blocks.append(f"[{index}] Source: {source}\n{item.content}")
        return "\n\n".join(blocks)

