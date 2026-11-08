from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("NICK_ENV", "development")
    log_level: str = os.getenv("NICK_LOG_LEVEL", "INFO")

def load_settings() -> Settings:
    return Settings()
