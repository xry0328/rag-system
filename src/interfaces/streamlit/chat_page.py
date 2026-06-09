from __future__ import annotations

import streamlit as st

from src.application.chat.commands import ChatCommand
from src.bootstrap.container import get_chat_service, get_knowledge_base_service, get_settings
from src.interfaces.streamlit.components import render_retrieved_contexts
from src.interfaces.streamlit.state import consume_async_iterator


def render() -> None:
    st.set_page_config(page_title="Customer Service Chat", layout="wide")
    st.title("Customer Service Chat")

    settings = get_settings()
    kb_service = get_knowledge_base_service()
    chat_service = get_chat_service()
    knowledge_bases = kb_service.list_knowledge_bases()

    with st.sidebar:
        st.subheader("Model")
        provider = st.selectbox(
            "Provider",
            options=["openai", "ollama", "xinference"],
            index=["openai", "ollama", "xinference"].index(settings.default_llm_provider)
            if settings.default_llm_provider in ["openai", "ollama", "xinference"]
            else 0,
        )
        default_model = {
            "openai": settings.openai_chat_model,
            "ollama": settings.ollama_chat_model,
            "xinference": settings.xinference_chat_model,
        }.get(provider, "")
        model = st.text_input("Model", value=default_model)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
        top_k = st.slider("Top K", 1, 12, settings.retrieval_top_k)

        st.subheader("Knowledge Bases")
        selected_kbs = st.multiselect(
            "Enabled knowledge bases",
            options=knowledge_bases,
            default=knowledge_bases[:1],
            format_func=lambda item: item.name,
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question")
    if not question:
        if not knowledge_bases:
            st.info("Create and ingest a knowledge base before chatting.")
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        tool_box = st.expander("Tool calls", expanded=True)
        answer_placeholder = st.empty()
        answer = ""
        contexts: list[dict] = []

        command = ChatCommand(
            question=question,
            knowledge_base_ids=[item.id for item in selected_kbs],
            provider=provider,
            model=model.strip() or None,
            temperature=temperature,
            top_k=top_k,
        )

        try:
            stream = chat_service.stream_answer(command)
            for event in consume_async_iterator(stream):
                if event.type == "tool_start":
                    with tool_box:
                        st.write(f"Calling tool: `{event.payload['tool']}`")
                elif event.type == "tool_end":
                    contexts = event.payload.get("contexts", [])
                    with tool_box:
                        st.write(f"Tool finished: `{event.payload['tool']}`")
                        render_retrieved_contexts(contexts)
                elif event.type == "token":
                    answer += event.payload.get("content", "")
                    answer_placeholder.markdown(answer)
                elif event.type == "error":
                    st.error(event.payload.get("message", "Unknown error."))
                elif event.type == "done":
                    break
        except Exception as exc:
            st.error(str(exc))
            answer = ""

        if answer:
            st.session_state.messages.append({"role": "assistant", "content": answer})

