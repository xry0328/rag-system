from __future__ import annotations

from pathlib import Path


class ChromaClientProvider:
    def __init__(self, persist_dir: Path) -> None:
        try:
            self._patch_sqlite_for_chroma()
            import chromadb
        except ImportError as exc:
            raise RuntimeError("Install chromadb to use the Chroma vector store.") from exc

        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_dir))

    def get_client(self):
        return self.client

    def _patch_sqlite_for_chroma(self) -> None:
        try:
            import pysqlite3
            import sys

            sys.modules["sqlite3"] = pysqlite3
        except ImportError:
            return
