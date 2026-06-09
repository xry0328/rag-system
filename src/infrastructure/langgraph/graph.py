from __future__ import annotations

from langgraph.graph import END, StateGraph

from src.infrastructure.langgraph.nodes import create_generate_node, create_retrieve_node
from src.infrastructure.langgraph.state import AgentState


def build_agent_graph(llm, retrieval_tool):
    graph = StateGraph(AgentState)
    graph.add_node("retrieve", create_retrieve_node(retrieval_tool))
    graph.add_node("generate", create_generate_node(llm))
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

