from __future__ import annotations


class KnowledgeBaseRetrievalTool:
    name = "knowledge_base_retrieval"

    def __init__(self, embedding_provider, retriever) -> None:
        self.embedding_provider = embedding_provider
        self.retriever = retriever

    def run(self, question: str, knowledge_base_ids: list[str], top_k: int):
        query_embedding = self.embedding_provider.embed_query(question)
        return self.retriever.search(query_embedding, knowledge_base_ids, top_k)

