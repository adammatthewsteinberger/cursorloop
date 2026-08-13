# cursorloop

[![PyPI](https://img.shields.io/pypi/v/cursorloop)](https://pypi.org/project/cursorloop/)
[![Python versions](https://img.shields.io/pypi/pyversions/cursorloop)](https://pypi.org/project/cursorloop/)
[![CI](https://github.com/adammatthewsteinberger/cursorloop/actions/workflows/ci.yml/badge.svg)](https://github.com/adammatthewsteinberger/cursorloop/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://adammatthewsteinberger.github.io/cursorloop/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/adammatthewsteinberger/cursorloop/blob/main/LICENSE)

**Onion-architected, autonomous Cursor Agent session runner** — Composer-first
(`composer-2.5`); Grok is a secondary **model profile**, not a product. Never
blocks on a human. Distinguishes a waitable rate-limit window from
non-waitable exhausted credits.

Same job as [claudeloop](https://github.com/adammatthewsteinberger/claudeloop),
retargeted onto the Cursor Agent SDK (`cursor-sdk`). **No Anthropic dependency.**

| | |
|---|---|
| Author | Adam Matthew Steinberger ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger)) |
| License | [MIT](https://github.com/adammatthewsteinberger/cursorloop/blob/main/LICENSE) |
| Docs | [adammatthewsteinberger.github.io/cursorloop](https://adammatthewsteinberger.github.io/cursorloop/) |
| Python | 3.12+ (macOS / Linux) |
| Default model | `composer-2.5` |
| Auth | `CURSOR_API_KEY` |
| Run state | `.cursorloop/` |

## Status (honest)

**Pre-1.0.** Tasks 1–20 are on `main`: Typer CLI (`run` / `resume` /
`doctor` / mid-run control), bootstrap auto-launches
`CursorClient.launch_bridge`, full doctor checklist (offline-capable),
deterministic `pytest -m system` harness, Cloud Agents **partial but live**
HTTP (`cloud me|models|…`, ADR-0006), CLI-fallback gateway, docs site, and
mirrored agent skills.

Use `CURSOR_API_KEY` for live runs, or the scripted test-agent gate for offline
end-to-end checks. `cursorloop doctor --offline` skips live `me` / models calls.

Start with the [quickstart](https://adammatthewsteinberger.github.io/cursorloop/getting-started/quickstart/)
or browse the [docs site](https://adammatthewsteinberger.github.io/cursorloop/).
Design history lives in the
[implementation plan](https://github.com/adammatthewsteinberger/cursorloop/blob/main/docs/superpowers/plans/2026-08-13-cursorloop-implementation.md)
(GitHub tree; not part of the published site nav).

## Install

```bash
pipx install cursorloop
# or
pip install cursorloop
```

From source:

```bash
git clone https://github.com/adammatthewsteinberger/cursorloop.git
cd cursorloop
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

See the [installation guide](https://adammatthewsteinberger.github.io/cursorloop/getting-started/installation/).

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

Coverage floors (CI): domain / application / infrastructure / CLI — **100%**.

## Non-negotiables

Documented in
[`AGENTS.md`](https://github.com/adammatthewsteinberger/cursorloop/blob/main/AGENTS.md)
/
[`CURSOR.md`](https://github.com/adammatthewsteinberger/cursorloop/blob/main/CURSOR.md):

1. Never block on a human.
2. Credits exhaustion ≠ waitable rate-limit window.
3. Capacity rejection always outranks a completion claim.
4. `domain/` stays pure (stdlib only).
5. No Anthropic / `claude_agent_sdk` dependency or foreign auth env fallbacks.

## Contributing

See [`CONTRIBUTING.md`](https://github.com/adammatthewsteinberger/cursorloop/blob/main/CONTRIBUTING.md).
PRs target **`develop`**.
Security:
[`SECURITY.md`](https://github.com/adammatthewsteinberger/cursorloop/blob/main/SECURITY.md).
Conduct:
[`CODE_OF_CONDUCT.md`](https://github.com/adammatthewsteinberger/cursorloop/blob/main/CODE_OF_CONDUCT.md).

## Plans

| Document | Purpose |
|---|---|
| [architecture-and-roadmap.md](https://github.com/adammatthewsteinberger/cursorloop/blob/main/docs/plans/architecture-and-roadmap.md) | Design record / transplant plan |
| [research-notes.md](https://github.com/adammatthewsteinberger/cursorloop/blob/main/docs/plans/research-notes.md) | Vendor SDK/CLI research |
| [_shared-transplant-outline.md](https://github.com/adammatthewsteinberger/cursorloop/blob/main/docs/plans/_shared-transplant-outline.md) | Cross-product keep/swap |
| [implementation plan](https://github.com/adammatthewsteinberger/cursorloop/blob/main/docs/superpowers/plans/2026-08-13-cursorloop-implementation.md) | Task-by-task TDD plan |

## License

MIT © Adam Matthew Steinberger. See
[LICENSE](https://github.com/adammatthewsteinberger/cursorloop/blob/main/LICENSE).
