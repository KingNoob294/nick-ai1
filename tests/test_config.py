from nick_ai.config import load_settings

def test_settings_load() -> None:
    settings = load_settings()
    assert settings.environment
    assert settings.log_level
