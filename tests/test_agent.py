from nick_ai.agent import Agent
from nick_ai.providers.base import Message, ModelResponse


class FakeProvider:
    name = "fake"

    def generate(self, messages: list[Message]) -> ModelResponse:
        assert messages[-1].role == "user"
        return ModelResponse("ok", "fake-model", self.name)


def test_agent_uses_provider():
    assert Agent(FakeProvider()).run("hello") == "ok"
