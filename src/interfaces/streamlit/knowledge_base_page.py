from __future__ import annotations

import streamlit as st

from src.application.knowledge_base.commands import CreateKnowledgeBaseCommand, IngestMarkdownCommand
from src.bootstrap.container import get_knowledge_base_service
from src.interfaces.streamlit.components import render_documents_table, render_knowledge_base_table


def render() -> None:
    st.set_page_config(page_title="Knowledge Base Management", layout="wide")
    st.title("Knowledge Base Management")

    service = get_knowledge_base_service()

    with st.form("create_knowledge_base"):
        st.subheader("Create Knowledge Base")
        name = st.text_input("Name")
        description = st.text_area("Description", height=80)
        submitted = st.form_submit_button("Create")
        if submitted:
            try:
                service.create_knowledge_base(CreateKnowledgeBaseCommand(name=name, description=description))
                st.success("Knowledge base created.")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    st.subheader("Knowledge Bases")
    knowledge_bases = service.list_knowledge_bases()
    render_knowledge_base_table(knowledge_bases)

    st.divider()
    st.subheader("Upload Markdown")
    if not knowledge_bases:
        st.info("Create a knowledge base before uploading documents.")
        return

    selected = st.selectbox(
        "Target knowledge base",
        options=knowledge_bases,
        format_func=lambda item: item.name,
    )
    uploads = st.file_uploader(
        "Markdown files",
        type=["md"],
        accept_multiple_files=True,
    )

    if st.button("Ingest selected files", type="primary", disabled=not uploads):
        for upload in uploads or []:
            with st.status(f"Ingesting {upload.name}", expanded=True) as status:
                try:
                    document = service.ingest_markdown(
                        IngestMarkdownCommand(
                            knowledge_base_id=selected.id,
                            filename=upload.name,
                            content=upload.getvalue(),
                        )
                    )
                    status.update(
                        label=f"Ingested {document.filename} into {document.chunk_count} chunks.",
                        state="complete",
                    )
                except Exception as exc:
                    status.update(label=f"Failed to ingest {upload.name}.", state="error")
                    st.error(str(exc))
        st.rerun()

    st.subheader("Documents")
    render_documents_table(service.list_documents(selected.id))

