from __future__ import annotations

from src.domain.shared.exceptions import InvalidMarkdownDocument


class DocumentDomainService:
    def validate_markdown(self, filename: str, content: bytes) -> None:
        if not filename.lower().endswith(".md"):
            raise InvalidMarkdownDocument("Only Markdown files with .md extension are supported.")
        if not content:
            raise InvalidMarkdownDocument("Uploaded Markdown file is empty.")

