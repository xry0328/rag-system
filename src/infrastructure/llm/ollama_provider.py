from __future__ import annotations


def create_ollama_chat_model(model: str, base_url: str, temperature: float):
    try:
        from langchain_ollama import ChatOllama
    except ImportError as exc:
        raise RuntimeError("Install langchain-ollama to use Ollama chat models.") from exc

    return ChatOllama(model=model, base_url=base_url, temperature=temperature)

