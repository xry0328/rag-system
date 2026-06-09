from __future__ import annotations

from collections.abc import AsyncIterator

from src.domain.chat.value_objects import AgentEvent
from src.infrastructure.langgraph.graph import build_agent_graph
from src.infrastructure.langgraph.tools import KnowledgeBaseRetrievalTool


class LangGraphAgentRunner:
    def __init__(self, llm, embedding_provider, retriever) -> None:
        retrieval_tool = KnowledgeBaseRetrievalTool(embedding_provider, retriever)
        self.graph = build_agent_graph(llm, retrieval_tool)

    async def stream(
        self,
        question: str,
        knowledge_base_ids: list[str],
        top_k: int,
    ) -> AsyncIterator[AgentEvent]:
        if not knowledge_base_ids:
            yield AgentEvent(type="error", payload={"message": "Please select at least one knowledge base."})
            return

        input_state = {
            "question": question,
            "knowledge_base_ids": knowledge_base_ids,
            "top_k": top_k,
            "contexts": [],
            "answer": "",
        }

        yielded_tool_start = False
        yielded_done = False
        async for event in self.graph.astream_events(input_state, version="v2"):
            event_type = event.get("event")
            name = event.get("name")

            if event_type == "on_chain_start" and name == "retrieve" and not yielded_tool_start:
                yielded_tool_start = True
                yield AgentEvent(type="tool_start", payload={"tool": "knowledge_base_retrieval"})

            if event_type == "on_chain_end" and name == "retrieve":
                output = event.get("data", {}).get("output", {})
                contexts = output.get("contexts", []) if isinstance(output, dict) else []
                yield AgentEvent(
                    type="tool_end",
                    payload={
                        "tool": "knowledge_base_retrieval",
                        "contexts": [context.__dict__ for context in contexts],
                    },
                )

            if event_type == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                content = getattr(chunk, "content", "")
                if isinstance(content, list):
                    content = "".join(str(part) for part in content)
                if content:
                    yield AgentEvent(type="token", payload={"content": content})

            if event_type == "on_chain_end" and name == "LangGraph":
                yielded_done = True
                yield AgentEvent(type="done", payload={})

        if not yielded_done:
            yield AgentEvent(type="done", payload={})

