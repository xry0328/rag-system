from __future__ import annotations

from src.infrastructure.llm.openai_provider import create_openai_chat_model


def create_xinference_chat_model(model: str, base_url: str, api_key: str, temperature: float):
    return create_openai_chat_model(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
    )

