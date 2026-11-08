from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ModelResponse:
    content: str
    model: str
    provider: str


class ModelProvider(Protocol):
    name: str

    def generate(self, messages: Sequence[Message]) -> ModelResponse:
        ...
