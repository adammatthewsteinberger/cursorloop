# cursorloop

**Onion-architected, autonomous Cursor Agent session runner** — Composer-first
(`composer-2.5`); Grok is a secondary **model profile**, not a product. Never
blocks on a human. Distinguishes a waitable rate-limit window from
non-waitable exhausted credits.

Same job as [claudeloop](https://github.com/adammatthewsteinberger/claudeloop),
retargeted onto the Cursor Agent SDK (`cursor-sdk`). No Anthropic dependency.

## Status

M1 scaffolding: installable package, onion import contracts, and the CI gate
set. Operator CLI and the autonomous runner land in later milestones.

## Install (from source)

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Auth env: `CURSOR_API_KEY`. Run state lives in `.cursorloop/`.

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

Coverage floors are passed per layer at the call site: domain 100%,
application 100%, infrastructure 85%, cli 85%.

## Plans

| Document | Purpose |
|---|---|
| [docs/plans/architecture-and-roadmap.md](docs/plans/architecture-and-roadmap.md) | Design record / transplant plan from claudeloop 0.5.4 |
| [docs/plans/research-notes.md](docs/plans/research-notes.md) | Vendor SDK/CLI capacity + autonomy research |
| [docs/plans/_shared-transplant-outline.md](docs/plans/_shared-transplant-outline.md) | Cross-product keep/swap + Global Constraints |
| [docs/superpowers/plans/2026-08-13-cursorloop-implementation.md](docs/superpowers/plans/2026-08-13-cursorloop-implementation.md) | Bite-sized TDD implementation plan |

## License

MIT. See [LICENSE](LICENSE).
