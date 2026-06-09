import streamlit as st


st.set_page_config(
    page_title="RAG Intelligent Customer Service",
    layout="wide",
)

st.title("RAG Intelligent Customer Service")
st.caption("DDD layered RAG system with Streamlit, LangGraph, Chroma, and pluggable models.")

st.markdown(
    """
    Use the pages in the sidebar:

    - Knowledge Base Management: create a knowledge base and ingest Markdown files.
    - Customer Service Chat: select knowledge bases, ask questions, and inspect tool calls.
    """
)
