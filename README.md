# Nick AI

Modular personal AI assistant foundation.

## Current stage

Provider-agnostic foundation for a personal AI assistant. Open-source and free components are preferred where practical.

## Architecture

- `src/nick_ai/` — core application
- `providers/` — model adapters
- `tools/` — controlled external capabilities
- `memory/` — persistent context
- `automation/` — scheduled/background tasks
- `tests/` — validation

## Principles

1. Prefer open-source and free components where practical.
2. Keep model providers replaceable.
3. Never commit secrets.
4. Add automation incrementally and test each layer.

Status: foundation phase.
