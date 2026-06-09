from __future__ import annotations


def create_openai_chat_model(model: str, api_key: str | None, base_url: str | None, temperature: float):
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError("Install langchain-openai to use OpenAI-compatible chat models.") from exc

    kwargs = {"model": model, "temperature": temperature, "streaming": True}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)

