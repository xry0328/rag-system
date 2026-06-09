from __future__ import annotations

from functools import lru_cache

from src.application.chat.service import ChatApplicationService
from src.application.knowledge_base.service import KnowledgeBaseApplicationService
from src.config.settings import settings
from src.infrastructure.embedding.factory import EmbeddingFactory, LazyEmbeddingProvider
from src.infrastructure.langgraph.streaming import LangGraphAgentRunner
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.loaders.markdown_loader import MarkdownLoader
from src.infrastructure.loaders.text_splitter import MarkdownTextSplitter
from src.infrastructure.persistence.file_store import LocalFileStore
from src.infrastructure.persistence.metadata_store import (
    DocumentJsonRepository,
    JsonMetadataStore,
    KnowledgeBaseJsonRepository,
)
from src.infrastructure.vectorstore.chroma_client import ChromaClientProvider
from src.infrastructure.vectorstore.chroma_repository import ChromaVectorRepository
from src.infrastructure.vectorstore.retriever import ChromaRetriever


@lru_cache(maxsize=1)
def get_settings():
    settings.ensure_dirs()
    return settings


@lru_cache(maxsize=1)
def get_metadata_store() -> JsonMetadataStore:
    return JsonMetadataStore(get_settings().metadata_file)


@lru_cache(maxsize=1)
def get_vector_repository() -> ChromaVectorRepository:
    client = ChromaClientProvider(get_settings().chroma_dir).get_client()
    return ChromaVectorRepository(client)


@lru_cache(maxsize=1)
def get_embedding_provider() -> LazyEmbeddingProvider:
    return LazyEmbeddingProvider(EmbeddingFactory(get_settings()))


@lru_cache(maxsize=1)
def get_retriever() -> ChromaRetriever:
    return ChromaRetriever(get_vector_repository())


@lru_cache(maxsize=1)
def get_knowledge_base_service() -> KnowledgeBaseApplicationService:
    metadata_store = get_metadata_store()
    return KnowledgeBaseApplicationService(
        knowledge_base_repository=KnowledgeBaseJsonRepository(metadata_store),
        document_repository=DocumentJsonRepository(metadata_store),
        file_store=LocalFileStore(get_settings().upload_dir),
        markdown_loader=MarkdownLoader(),
        text_splitter=MarkdownTextSplitter(
            chunk_size=get_settings().chunk_size,
            chunk_overlap=get_settings().chunk_overlap,
        ),
        embedding_provider=get_embedding_provider(),
        vector_repository=get_vector_repository(),
    )


@lru_cache(maxsize=1)
def get_chat_service() -> ChatApplicationService:
    return ChatApplicationService(
        llm_factory=LLMFactory(get_settings()),
        embedding_provider=get_embedding_provider(),
        retriever=get_retriever(),
        agent_runner_factory=LangGraphAgentRunner,
    )

