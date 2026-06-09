from __future__ import annotations

from src.domain.document.entities import DocumentChunk


class ChromaVectorRepository:
    def __init__(self, client) -> None:
        self.client = client

    def ensure_collection(self, knowledge_base_id: str):
        return self.client.get_or_create_collection(name=self._collection_name(knowledge_base_id))

    def add_chunks(
        self,
        knowledge_base_id: str,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if not chunks:
            return
        collection = self.ensure_collection(knowledge_base_id)
        collection.add(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=embeddings,
            metadatas=[chunk.metadata for chunk in chunks],
        )

    def query(self, knowledge_base_id: str, query_embedding: list[float], top_k: int) -> dict:
        collection = self.ensure_collection(knowledge_base_id)
        return collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    def _collection_name(self, knowledge_base_id: str) -> str:
        return knowledge_base_id.replace("-", "_")[:63]

