from __future__ import annotations

from src.domain.document.value_objects import SplitDocument


class MarkdownTextSplitter:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = min(chunk_overlap, max(chunk_size - 1, 0))

    def split(self, text: str) -> list[SplitDocument]:
        normalized = text.replace("\r\n", "\n").strip()
        if not normalized:
            return []

        chunks: list[SplitDocument] = []
        start = 0
        index = 0
        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))
            if end < len(normalized):
                paragraph_break = normalized.rfind("\n\n", start, end)
                heading_break = normalized.rfind("\n#", start, end)
                split_at = max(paragraph_break, heading_break)
                if split_at > start + self.chunk_size // 2:
                    end = split_at

            content = normalized[start:end].strip()
            if content:
                chunks.append(SplitDocument(content=content, metadata={"chunk_index": index}))
                index += 1

            if end >= len(normalized):
                break
            start = max(end - self.chunk_overlap, start + 1)

        return chunks

