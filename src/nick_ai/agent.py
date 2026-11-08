from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .providers.base import Message, ModelProvider


@dataclass
class Agent:
    provider: ModelProvider
    system_prompt: str = (
        "You are Nick AI, a practical personal assistant. "
        "Be concise, accurate, and transparent about uncertainty."
    )

    def run(self, user_input: str, history: Sequence[Message] = ()) -> str:
        messages = [Message("system", self.system_prompt), *history, Message("user", user_input)]
        response = self.provider.generate(messages)
        return response.content
