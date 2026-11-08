from .config import load_settings

def run() -> None:
    settings = load_settings()
    print(f"Nick AI {settings.environment} - foundation ready")

if __name__ == "__main__":
    run()
