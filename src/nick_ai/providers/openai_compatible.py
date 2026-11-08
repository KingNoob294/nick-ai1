from __future__ import annotations

import json
from urllib.request import Request, urlopen

from .base import Message, ModelResponse


class OpenAICompatibleProvider:
    """Adapter for OpenAI-compatible chat completion APIs."""

    name = "openai_compatible"

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 90.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, messages: list[Message] | tuple[Message, ...]) -> ModelResponse:
        if not self.api_key:
            raise RuntimeError("NICK_API_KEY is missing. Add a provider API key in the hosting environment.")
        payload = {
            "model": self.model,
            "messages": [{"role": item.role, "content": item.content} for item in messages],
            "temperature": 0.4,
        }
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Model provider request failed: {exc}") from exc
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Model provider returned an unexpected response.") from exc
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Model provider returned an empty response.")
        return ModelResponse(content=content.strip(), model=self.model, provider=self.name)
