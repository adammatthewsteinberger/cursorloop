# Changelog

## [0.1.0](https://github.com/adammatthewsteinberger/cursorloop/releases/tag/v0.1.0) (unreleased)

First public release of **cursorloop**: an onion-architected, autonomous
Cursor Agent session runner. Composer-first (`composer-2.5`); Grok is a
secondary model profile. Never blocks on a human; distinguishes waitable
rate-limit windows from exhausted credits.

### Features

- Typer CLI (`run` / `resume` / `doctor` / mid-run control / `cloud` subset)
- Durable Cursor SDK bridge with capacity taxonomy and empty-turn soft-fail
- Scripted test-agent gate, system harness, and live doctor checklist
- Partial Cloud Agents OpenAPI surface (live HTTP for me/models/create/get/cancel)
