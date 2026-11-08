import os

import uvicorn


def run() -> None:
    uvicorn.run(
        "nick_ai.webapp:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("NICK_ENV", "development") == "development",
    )


if __name__ == "__main__":
    run()
