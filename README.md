# Nick AI

A modular personal AI assistant with a mobile-friendly Persian chat interface, replaceable model providers, persistent conversation history, and a small allow-listed tool system.

## Current capabilities

- FastAPI web server and responsive Persian chat page.
- OpenAI-compatible provider (Hugging Face Inference Providers, OpenRouter, or compatible gateways).
- Ollama provider for a self-hosted model.
- SQLite conversation history, separated by browser session.
- Built-in commands: `/help`, `/time`, and safe arithmetic with `/calc 12*(3+4)`.
- Optional Bearer-token protection for the HTTP API.
- Automated tests with GitHub Actions.

## Run locally

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Set environment variables from `.env.example` in your shell or hosting dashboard, then run:

```bash
nick-ai
```

Open `http://localhost:8000`.

On Windows, activate the environment with `.venv\\Scripts\\activate`.

## Configure a hosted model

Set these environment variables in the hosting provider:

- `NICK_PROVIDER=openai_compatible`
- `NICK_API_BASE=https://router.huggingface.co/v1`
- `NICK_API_KEY` to your private provider token
- `NICK_MODEL` to a model currently supported by that provider

The model endpoint and model availability depend on the inference provider, account limits, and region. A free tier is not guaranteed to have unlimited or uninterrupted inference. Never commit API tokens to GitHub.

For Ollama, set `NICK_PROVIDER=ollama`, `NICK_OLLAMA_URL` to the reachable Ollama server URL, and `NICK_MODEL` to an installed model name. Ollama must be reachable from the machine running Nick AI; localhost on a cloud host is not your phone.

## Deploy from a phone with Render

1. Sign in to Render and choose **New + → Blueprint**.
2. Connect the GitHub repository `KingNoob294/nick-ai1`.
3. Let Render read `render.yaml` and create the web service.
4. In the service environment settings, add `NICK_API_KEY` as a secret. Choose a supported model/provider and update `NICK_MODEL` if necessary.
5. Wait for deployment, then open the service URL. The chat page is the home page; `/health` checks server status.

The free web service may sleep when idle. Its local filesystem can be temporary, so SQLite history may be lost after a restart or redeploy. Persistent memory for long-term use needs a persistent disk or managed database. Do not put private keys or personal sensitive data into a public demo.

## API

- `GET /health` — service and provider status (never returns the secret).
- `POST /api/chat` — JSON body: `{"message":"Hello","session_id":"a-long-random-session-id"}`.
- `DELETE /api/history/{session_id}` — clear one session's stored chat history.

If `NICK_API_TOKEN` is set, send `Authorization: Bearer YOUR_TOKEN` with API requests. The built-in browser page is intended for a private demo with this setting left empty; do not expose a token-protected deployment publicly until a login flow is configured.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Safety and roadmap

Nick AI only runs explicit, allow-listed local commands. It does not execute arbitrary shell commands, modify its own source, or autonomously deploy code. Browser automation, scheduled jobs, broader memory controls, and self-update workflows should be added behind explicit permissions and tests.

Status: first runnable MVP; deployment and live model credentials are configured by the repository owner.
