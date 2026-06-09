from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage

from src.config.prompts import ANSWER_PROMPT_TEMPLATE, SYSTEM_PROMPT
from src.domain.chat.services import ChatDomainService


def create_retrieve_node(retrieval_tool):
    def retrieve(state: dict) -> dict:
        contexts = retrieval_tool.run(
            question=state["question"],
            knowledge_base_ids=state["knowledge_base_ids"],
            top_k=state["top_k"],
        )
        return {"contexts": contexts}

    return retrieve


def create_generate_node(llm):
    chat_domain_service = ChatDomainService()

    async def generate(state: dict) -> dict:
        context_block = chat_domain_service.build_context_block(state.get("contexts", []))
        prompt = ANSWER_PROMPT_TEMPLATE.format(question=state["question"], context=context_block)
        response = await llm.ainvoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)])
        return {"answer": response.content}

    return generate

