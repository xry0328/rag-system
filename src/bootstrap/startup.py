from __future__ import annotations

from src.bootstrap.container import get_settings


def initialize_app() -> None:
    get_settings().ensure_dirs()

