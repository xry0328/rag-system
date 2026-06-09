from __future__ import annotations

from src.config.settings import Settings
from src.infrastructure.embedding.openai_embedding import OpenAIEmbeddingProvider


class EmbeddingFactory:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create_default(self) -> OpenAIEmbeddingProvider:
        return OpenAIEmbeddingProvider(
            model=self.settings.openai_embedding_model,
            api_key=self.settings.openai_api_key,
            base_url=self.settings.openai_base_url,
        )


class LazyEmbeddingProvider:
    def __init__(self, factory: EmbeddingFactory) -> None:
        self.factory = factory
        self._provider = None

    def _get_provider(self):
        if self._provider is None:
            self._provider = self.factory.create_default()
        return self._provider

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._get_provider().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._get_provider().embed_query(text)
