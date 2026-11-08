from nick_ai.config import Settings
from nick_ai.providers.base import Message, ModelResponse
from nick_ai.webapp import create_app
from fastapi.testclient import TestClient


class FakeProvider:
    name = "fake"

    def generate(self, messages):
        assert messages[-1].role == "user"
        return ModelResponse("پاسخ آزمایشی نیک", "fake-model", self.name)


def make_settings(database_path):
    return Settings(
        environment="test",
        log_level="INFO",
        provider="openai_compatible",
        api_base="https://example.invalid/v1",
        api_key="test-key",
        model="fake-model",
        ollama_url="http://localhost:11434",
        database_path=str(database_path),
        request_timeout=2,
        max_history=8,
        api_token="",
    )


def test_health_and_chat(tmp_path):
    app = create_app(make_settings(tmp_path / "test.db"), provider=FakeProvider())
    client = TestClient(app)
    assert client.get("/health").json()["status"] == "ok"
    response = client.post(
        "/api/chat",
        json={"message": "سلام", "session_id": "test-session-123"},
    )
    assert response.status_code == 200
    assert response.json()["reply"] == "پاسخ آزمایشی نیک"


def test_builtin_command(tmp_path):
    app = create_app(make_settings(tmp_path / "tools.db"), provider=FakeProvider())
    client = TestClient(app)
    response = client.post(
        "/api/chat",
        json={"message": "/calc 5*5", "session_id": "test-session-456"},
    )
    assert response.status_code == 200
    assert response.json()["reply"] == "25"
    assert response.json()["provider"] == "local-tool"
