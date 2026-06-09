from __future__ import annotations

import re
from pathlib import Path


class LocalFileStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, knowledge_base_id: str, filename: str, content: bytes) -> Path:
        target_dir = self.root / knowledge_base_id
        target_dir.mkdir(parents=True, exist_ok=True)
        safe_name = self._safe_filename(filename)
        target = target_dir / safe_name
        target.write_bytes(content)
        return target

    def _safe_filename(self, filename: str) -> str:
        name = Path(filename).name
        return re.sub(r"[^A-Za-z0-9._-]", "_", name)

