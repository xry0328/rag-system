from __future__ import annotations

from src.domain.chat.value_objects import RetrievedContext


class ChromaRetriever:
    def __init__(self, vector_repository) -> None:
        self.vector_repository = vector_repository

    def search(
        self,
        query_embedding: list[float],
        knowledge_base_ids: list[str],
        top_k: int,
    ) -> list[RetrievedContext]:
        contexts: list[RetrievedContext] = []
        for knowledge_base_id in knowledge_base_ids:
            result = self.vector_repository.query(knowledge_base_id, query_embedding, top_k)
            documents = result.get("documents", [[]])[0]
            metadatas = result.get("metadatas", [[]])[0]
            distances = result.get("distances", [[]])[0]
            ids = result.get("ids", [[]])[0]
            for content, metadata, distance, chunk_id in zip(documents, metadatas, distances, ids):
                metadata = metadata or {}
                contexts.append(
                    RetrievedContext(
                        content=content,
                        score=float(distance) if distance is not None else None,
                        knowledge_base_id=metadata.get("knowledge_base_id", knowledge_base_id),
                        document_id=metadata.get("document_id", ""),
                        chunk_id=chunk_id,
                        filename=metadata.get("filename", ""),
                        metadata=metadata,
                    )
                )
        contexts.sort(key=lambda item: item.score if item.score is not None else float("inf"))
        return contexts[:top_k]

