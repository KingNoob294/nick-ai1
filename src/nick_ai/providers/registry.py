from __future__ import annotations

from .base import ModelProvider
from .ollama import OllamaProvider
from .openai_compatible import OpenAICompatibleProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {}

    def register(self, provider: ModelProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> ModelProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._providers)) or "none"
            raise ValueError(f"Unknown provider '{name}'. Available: {available}") from exc


def build_default_registry(
    provider_name: str = "openai_compatible",
    api_base: str = "https://router.huggingface.co/v1",
    api_key: str = "",
    model: str = "Qwen/Qwen2.5-7B-Instruct",
    ollama_url: str = "http://localhost:11434",
    timeout: float = 90.0,
) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(OpenAICompatibleProvider(api_base, api_key, model, timeout))
    registry.register(OllamaProvider(ollama_url, model, timeout))
    if provider_name not in ("openai_compatible", "ollama"):
        raise ValueError("NICK_PROVIDER must be 'openai_compatible' or 'ollama'")
    return registry
