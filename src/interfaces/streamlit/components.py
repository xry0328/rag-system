from __future__ import annotations

import streamlit as st


def render_knowledge_base_table(knowledge_bases) -> None:
    if not knowledge_bases:
        st.info("No knowledge bases yet. Create one to start ingesting Markdown documents.")
        return

    st.dataframe(
        [
            {
                "Name": item.name,
                "Description": item.description,
                "Documents": item.document_count,
                "Chunks": item.chunk_count,
                "Updated": item.updated_at,
                "ID": item.id,
            }
            for item in knowledge_bases
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_documents_table(documents) -> None:
    if not documents:
        st.caption("No documents have been ingested into this knowledge base.")
        return

    st.dataframe(
        [
            {
                "Filename": item.filename,
                "Status": item.status,
                "Chunks": item.chunk_count,
                "Error": item.error,
                "Updated": item.updated_at,
            }
            for item in documents
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_retrieved_contexts(contexts: list[dict]) -> None:
    if not contexts:
        st.caption("No relevant chunks were returned.")
        return

    for index, context in enumerate(contexts, start=1):
        score = context.get("score")
        filename = context.get("filename") or "Unknown source"
        label = f"{index}. {filename}"
        if score is not None:
            label += f" | distance {score:.4f}"
        with st.expander(label, expanded=index == 1):
            st.write(context.get("content", ""))

