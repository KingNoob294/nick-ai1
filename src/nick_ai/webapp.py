from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel, Field

from .agent import Agent
from .config import Settings, load_settings
from .memory import MemoryStore
from .providers.registry import build_default_registry
from .tools import ToolRegistry


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    session_id: str = Field(min_length=8, max_length=80)


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    provider: str
    model: str


def create_app(
    settings: Settings | None = None,
    provider=None,
    memory: MemoryStore | None = None,
) -> FastAPI:
    settings = settings or load_settings()
    registry = build_default_registry(
        provider_name=settings.provider,
        api_base=settings.api_base,
        api_key=settings.api_key,
        model=settings.model,
        ollama_url=settings.ollama_url,
        timeout=settings.request_timeout,
    )
    selected_provider = provider or registry.get(settings.provider)
    store = memory or MemoryStore(settings.database_path)
    tools = ToolRegistry()

    app = FastAPI(title="Nick AI", version="0.2.0")
    app.state.memory = store
    app.state.provider = selected_provider

    def authorize(authorization: str | None) -> None:
        if settings.api_token and authorization != f"Bearer {settings.api_token}":
            raise HTTPException(status_code=401, detail="Unauthorized")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "app": "Nick AI",
            "provider": selected_provider.name,
            "model": settings.model,
            "api_key_configured": bool(settings.api_key) or settings.provider == "ollama",
        }

    @app.get("/")
    def home():
        return FileResponse(Path(__file__).resolve().parents[2] / "web" / "index.html")

    @app.post("/api/chat", response_model=ChatResponse)
    def chat(payload: ChatRequest, authorization: str | None = Header(default=None)):
        authorize(authorization)
        command_result = tools.execute_command(payload.message)
        if command_result is not None:
            store.add(payload.session_id, "user", payload.message)
            store.add(payload.session_id, "assistant", command_result)
            return ChatResponse(
                reply=command_result,
                session_id=payload.session_id,
                provider="local-tool",
                model="built-in",
            )

        history = store.history(payload.session_id, settings.max_history)
        try:
            reply = Agent(selected_provider).run(payload.message, history)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        store.add(payload.session_id, "user", payload.message)
        store.add(payload.session_id, "assistant", reply)
        return ChatResponse(
            reply=reply,
            session_id=payload.session_id,
            provider=selected_provider.name,
            model=settings.model,
        )

    @app.delete("/api/history/{session_id}")
    def clear_history(session_id: str, authorization: str | None = Header(default=None)):
        authorize(authorization)
        if not 8 <= len(session_id) <= 80:
            raise HTTPException(status_code=400, detail="Invalid session id")
        store.clear(session_id)
        return {"status": "cleared"}

    return app


app = create_app()
