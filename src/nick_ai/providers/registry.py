from __future__ import annotations

from .base import ModelProvider
from .ollama import OllamaProvider


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
    ollama_url: str = "http://localhost:11434",
    ollama_model: str = "qwen2.5:3b",
) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(OllamaProvider(ollama_url, ollama_model))
    return registry
