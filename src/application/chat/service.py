from __future__ import annotations

from collections.abc import AsyncIterator

from src.application.chat.commands import ChatCommand
from src.domain.chat.value_objects import AgentEvent


class ChatApplicationService:
    def __init__(self, llm_factory, embedding_provider, retriever, agent_runner_factory) -> None:
        self.llm_factory = llm_factory
        self.embedding_provider = embedding_provider
        self.retriever = retriever
        self.agent_runner_factory = agent_runner_factory

    async def stream_answer(self, command: ChatCommand) -> AsyncIterator[AgentEvent]:
        llm = self.llm_factory.create(command.provider, command.model, command.temperature)
        runner = self.agent_runner_factory(llm, self.embedding_provider, self.retriever)
        async for event in runner.stream(
            question=command.question,
            knowledge_base_ids=command.knowledge_base_ids,
            top_k=command.top_k,
        ):
            yield event

