from src.infrastructure.loaders.text_splitter import MarkdownTextSplitter


def test_markdown_text_splitter_preserves_content_order():
    splitter = MarkdownTextSplitter(chunk_size=30, chunk_overlap=5)
    chunks = splitter.split("# Title\n\nFirst paragraph.\n\nSecond paragraph.")

    assert chunks
    assert chunks[0].content.startswith("# Title")
    assert [chunk.metadata["chunk_index"] for chunk in chunks] == list(range(len(chunks)))

