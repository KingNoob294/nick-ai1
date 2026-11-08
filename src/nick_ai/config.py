from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    environment: str
    log_level: str
    provider: str
    api_base: str
    api_key: str
    model: str
    ollama_url: str
    database_path: str
    request_timeout: float
    max_history: int
    api_token: str


def load_settings() -> Settings:
    return Settings(
        environment=os.getenv("NICK_ENV", "development"),
        log_level=os.getenv("NICK_LOG_LEVEL", "INFO"),
        provider=os.getenv("NICK_PROVIDER", "openai_compatible").lower(),
        api_base=os.getenv("NICK_API_BASE", "https://router.huggingface.co/v1"),
        api_key=os.getenv("NICK_API_KEY", ""),
        model=os.getenv("NICK_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        ollama_url=os.getenv("NICK_OLLAMA_URL", "http://localhost:11434"),
        database_path=os.getenv("NICK_DATABASE_PATH", "data/nick_ai.db"),
        request_timeout=float(os.getenv("NICK_REQUEST_TIMEOUT", "90")),
        max_history=max(1, int(os.getenv("NICK_MAX_HISTORY", "12"))),
        api_token=os.getenv("NICK_API_TOKEN", ""),
    )
