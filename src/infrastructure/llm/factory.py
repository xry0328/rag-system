from __future__ import annotations

from src.config.settings import Settings
from src.infrastructure.llm.ollama_provider import create_ollama_chat_model
from src.infrastructure.llm.openai_provider import create_openai_chat_model
from src.infrastructure.llm.xinference_provider import create_xinference_chat_model


class LLMFactory:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create(self, provider: str, model: str | None, temperature: float):
        normalized = provider.strip().lower()
        if normalized == "openai":
            return create_openai_chat_model(
                model=model or self.settings.openai_chat_model,
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_base_url,
                temperature=temperature,
            )
        if normalized == "ollama":
            return create_ollama_chat_model(
                model=model or self.settings.ollama_chat_model,
                base_url=self.settings.ollama_base_url,
                temperature=temperature,
            )
        if normalized == "xinference":
            chosen_model = model or self.settings.xinference_chat_model
            if not chosen_model:
                raise ValueError("Xinference model is required. Set XINFERENCE_CHAT_MODEL or enter it in the UI.")
            return create_xinference_chat_model(
                model=chosen_model,
                base_url=self.settings.xinference_base_url,
                api_key=self.settings.xinference_api_key,
                temperature=temperature,
            )
        raise ValueError(f"Unsupported LLM provider: {provider}")

