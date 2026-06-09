from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "RAG Intelligent Customer Service")
    project_root: Path = PROJECT_ROOT
    data_dir: Path = PROJECT_ROOT / "data"
    upload_dir: Path = PROJECT_ROOT / "data" / "uploads"
    chroma_dir: Path = PROJECT_ROOT / "data" / "chroma"
    metadata_dir: Path = PROJECT_ROOT / "data" / "metadata"
    metadata_file: Path = PROJECT_ROOT / "data" / "metadata" / "registry.json"

    default_llm_provider: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")

    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or None
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL") or None
    openai_chat_model: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:7b")

    xinference_base_url: str = os.getenv("XINFERENCE_BASE_URL", "http://localhost:9997/v1")
    xinference_api_key: str = os.getenv("XINFERENCE_API_KEY", "xinference")
    xinference_chat_model: str = os.getenv("XINFERENCE_CHAT_MODEL", "")

    chunk_size: int = _int_env("CHUNK_SIZE", 900)
    chunk_overlap: int = _int_env("CHUNK_OVERLAP", 120)
    retrieval_top_k: int = _int_env("RETRIEVAL_TOP_K", 5)

    def ensure_dirs(self) -> None:
        for path in [self.upload_dir, self.chroma_dir, self.metadata_dir]:
            path.mkdir(parents=True, exist_ok=True)


settings = Settings()

