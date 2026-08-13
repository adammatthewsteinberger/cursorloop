# Contributing to cursorloop

Thank you for considering a contribution. This document is command-level —
if something here is unclear, that is a bug in this document; please open an
issue or a PR fixing it.

## Environment setup

```bash
git clone https://github.com/adammatthewsteinberger/cursorloop.git
cd cursorloop
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Requires **Python 3.12+** on **macOS or Linux**. Windows is not a supported
target. Auth for live Cursor runs: `CURSOR_API_KEY` (never a foreign vendor
API-key env var).

## Branch model

```
main         ← always releasable
  ▲
develop      ← integration branch; open PRs here
  ▲
feature/*    ← your work
```

1. Branch from `develop`: `git checkout -b feature/short-description develop`
2. Use [Conventional Commits](https://www.conventionalcommits.org/).
3. Open a PR **into `develop`**, not `main`.
4. Feature PRs are **squash-merged**; release merges into `main` preserve history.

## Quality gates

Local (also enforced by pre-commit + CI):

```bash
ruff check src tests
ruff format --check src tests
mypy src/cursorloop
pytest
lint-imports
bandit -q -r src/cursorloop
pip-audit
```

Coverage floors (pass `--cov` / `--cov-fail-under` per layer as CI does):
domain **100%**, application **100%**, infrastructure **85%**, cli **85%**.

## Onion import rule

Dependencies point inward only:

```
domain → application → infrastructure → cli
```

`bootstrap.py` is the sole composition root. `domain/` is stdlib-only (no I/O,
no async, no third-party imports) — enforced by `import-linter`, not convention.

## Non-negotiables (do not regress these)

- Never block on a human.
- Exhausted credits ≠ waitable rate-limit window (`CreditsExhausted` has no reset).
- A capacity rejection always outranks a completion claim.
- No Anthropic / `claude_agent_sdk` dependency; no foreign vendor auth env fallbacks.
- Default model profile is `composer-2.5`; Grok is a profile, not a product.

## PR checklist

- [ ] Targets `develop`
- [ ] Conventional Commits (commits or squash title)
- [ ] `pre-commit run --all-files` passes
- [ ] Tests + coverage floors green for touched layers
- [ ] Docs updated if behavior changed
- [ ] Agree to the [Code of Conduct](CODE_OF_CONDUCT.md) and MIT licensing of the contribution

## License of contributions

By contributing, you agree your contributions are licensed under the MIT
License (same as the project). Copyright (c) Adam Matthew Steinberger.

## Getting help

- Bugs / features: GitHub Issues
- Design context: `docs/plans/architecture-and-roadmap.md`
- Implementation plan: `docs/superpowers/plans/2026-08-13-cursorloop-implementation.md`
