# cursorloop

[![CI](https://github.com/adammatthewsteinberger/cursorloop/actions/workflows/ci.yml/badge.svg)](https://github.com/adammatthewsteinberger/cursorloop/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Onion-architected, autonomous Cursor Agent session runner** — Composer-first
(`composer-2.5`); Grok is a secondary **model profile**, not a product. Never
blocks on a human. Distinguishes a waitable rate-limit window from
non-waitable exhausted credits.

Same job as [claudeloop](https://github.com/adammatthewsteinberger/claudeloop),
retargeted onto the Cursor Agent SDK (`cursor-sdk`). **No Anthropic dependency.**

| | |
|---|---|
| Author | Adam Matthew Steinberger ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger)) |
| License | [MIT](LICENSE) |
| Python | 3.12+ (macOS / Linux) |
| Default model | `composer-2.5` |
| Auth | `CURSOR_API_KEY` |
| Run state | `.cursorloop/` |

## Status (honest)

**Pre-1.0 / mid-implementation.** Domain + application runner + Cursor agent
adapters + supporting control-plane infra are in place and covered by tests.
The operator CLI composition root (`bootstrap` / Typer commands / `doctor`) is
still landing — the console script currently exits 0 as a packaging stub.

See the [implementation plan](docs/superpowers/plans/2026-08-13-cursorloop-implementation.md)
for remaining tasks (CLI, doctor, M3 UX, optional M4/M5 sketches).

## Install (from source)

```bash
git clone https://github.com/adammatthewsteinberger/cursorloop.git
cd cursorloop
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Quality gates

```bash
ruff check src tests
ruff format --check src tests
mypy src/cursorloop
pytest
lint-imports
bandit -q -r src/cursorloop
pip-audit
```

Coverage floors (CI): domain 100%, application 100%, infrastructure 85%,
cli 85%.

## Non-negotiables

Documented in [`AGENTS.md`](AGENTS.md) / [`CURSOR.md`](CURSOR.md):

1. Never block on a human.
2. Credits exhaustion ≠ waitable rate-limit window.
3. Capacity rejection always outranks a completion claim.
4. `domain/` stays pure (stdlib only).
5. No Anthropic / `claude_agent_sdk` dependency or foreign auth env fallbacks.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). PRs target **`develop`**.
Security reports: [`SECURITY.md`](SECURITY.md). Conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Plans

| Document | Purpose |
|---|---|
| [architecture-and-roadmap.md](docs/plans/architecture-and-roadmap.md) | Design record / transplant plan |
| [research-notes.md](docs/plans/research-notes.md) | Vendor SDK/CLI research |
| [_shared-transplant-outline.md](docs/plans/_shared-transplant-outline.md) | Cross-product keep/swap |
| [implementation plan](docs/superpowers/plans/2026-08-13-cursorloop-implementation.md) | Task-by-task TDD plan |

## License

MIT © Adam Matthew Steinberger. See [LICENSE](LICENSE).
