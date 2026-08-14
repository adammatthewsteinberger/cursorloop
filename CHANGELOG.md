# Changelog

## [0.3.0](https://github.com/adammatthewsteinberger/cursorloop/compare/cursorloop-v0.2.0...cursorloop-v0.3.0) (2026-08-14)


### Features

* **application:** add the autonomous runner with probe-based recovery and fault handling ([ec978bf](https://github.com/adammatthewsteinberger/cursorloop/commit/ec978bf6a3f484e3cdc5c59825183bcbee0c7eb7))
* **application:** declare protocol ports, DTOs, and the port fakes ([b31523d](https://github.com/adammatthewsteinberger/cursorloop/commit/b31523d3695ecfaf1958da26a8b82a2b890bf8ab))
* complete Tasks 16–20 (CLI, doctor, system harness, M4/M5) ([#1](https://github.com/adammatthewsteinberger/cursorloop/issues/1)) ([51d237b](https://github.com/adammatthewsteinberger/cursorloop/commit/51d237b3c53c51f6a88a476265cac1a2833ab4ba))
* complete Tasks 16–20 (CLI, doctor, system harness, M4/M5) ([#1](https://github.com/adammatthewsteinberger/cursorloop/issues/1)) ([936df1e](https://github.com/adammatthewsteinberger/cursorloop/commit/936df1e8f3d8294210eacc69a3f2037e23eccc76))
* **domain:** add adaptive probe scheduling with credits backoff and window bounds ([64fbf33](https://github.com/adammatthewsteinberger/cursorloop/commit/64fbf33e1afd634a6ca976ce8b9eb80dba06ee42))
* **domain:** add budget ledger, model profiles, agent selectors, and hook policy ([5a40513](https://github.com/adammatthewsteinberger/cursorloop/commit/5a40513dd025e93dee6756b9e49b1510f0640c9c))
* **domain:** add CapacityState and Fault algebraic data types ([5fe6f9d](https://github.com/adammatthewsteinberger/cursorloop/commit/5fe6f9df3c5dd3ab44c273823b93870993a50b29))
* **domain:** add the pure run-loop state machine with capacity-outranks-verdict ordering ([83e671f](https://github.com/adammatthewsteinberger/cursorloop/commit/83e671f2ca19f0a418210786a41a577586a06141))
* **domain:** classify Cursor turn signals into capacity states and faults ([1d057b1](https://github.com/adammatthewsteinberger/cursorloop/commit/1d057b132b29aa52c73f13fc73aeb7c53db31ded))
* **domain:** detect completion via verdict block, marker fallback, and plan reconciliation ([3436c03](https://github.com/adammatthewsteinberger/cursorloop/commit/3436c038a424ead2d55775d7b759bf27aecebab1))
* **domain:** parse Retry-After and add configurable billing/rate-limit lexicons ([4b87be2](https://github.com/adammatthewsteinberger/cursorloop/commit/4b87be2acd56a2dd54b28d42ddd193b83b72c25e))
* **infra:** add logging, redaction, run state, locking, audit, and config adapters ([22af255](https://github.com/adammatthewsteinberger/cursorloop/commit/22af255d29e5c5b48d9272475c49d185dbf34b00))
* **infra:** add the Cursor agent gateway, capacity probe, stall watchdog, and catalogs ([25ead2f](https://github.com/adammatthewsteinberger/cursorloop/commit/25ead2f7fa508281527683eb86dac21a14c452d9))
* **infra:** build Cursor agent options from a single create/resume builder ([72405ee](https://github.com/adammatthewsteinberger/cursorloop/commit/72405eeff2e93e23798faa2c8f066ad5fe04f1bc))
* **infra:** manage .cursor/hooks.json autonomy fragment with hash-verified restore ([a36bba2](https://github.com/adammatthewsteinberger/cursorloop/commit/a36bba2a7d5cdb5887f1822555050d13a421a118))
* **infra:** translate Cursor SDK runs and errors into turn signals ([e28b7ce](https://github.com/adammatthewsteinberger/cursorloop/commit/e28b7ce71b0256e6eca2e1f15fd75d0292c50850))


### Bug Fixes

* **application:** cap send-path Busy retries with jittered backoff ([8236ae7](https://github.com/adammatthewsteinberger/cursorloop/commit/8236ae70af7e377de24ffb43750edabd21bf8fc3))
* **application:** jitter transient backoff and always release runner resources ([eae2fd3](https://github.com/adammatthewsteinberger/cursorloop/commit/eae2fd302a845ffbd3c54bde0a64b07747995b2a))
* **ci:** build TestPyPI from develop; PyPI stays release/main-only ([#6](https://github.com/adammatthewsteinberger/cursorloop/issues/6)) ([89c82cb](https://github.com/adammatthewsteinberger/cursorloop/commit/89c82cb641b3452288d549d15cff4b9c9a2f8334))
* **ci:** build TestPyPI from develop; PyPI stays release/main-only ([#6](https://github.com/adammatthewsteinberger/cursorloop/issues/6)) ([73473be](https://github.com/adammatthewsteinberger/cursorloop/commit/73473be9f5e6d9184bcd3660c262a559b4a24e81))
* **domain:** default turn cost to unknown and enforce wall-clock while waiting ([1f2aa12](https://github.com/adammatthewsteinberger/cursorloop/commit/1f2aa121aca956eae7f0a54573d1daf09db6707e))
* **domain:** never raise from parse_retry_after on nan or mixed-offset datetimes ([26b4eb1](https://github.com/adammatthewsteinberger/cursorloop/commit/26b4eb1d38a120c7863ed6fc9d8dd4a6b9f71ef1))
* **infra:** complete a recorded-but-unapplied hooks install on retry ([0c1d1ed](https://github.com/adammatthewsteinberger/cursorloop/commit/0c1d1ede399e96d0a6290b853ca562362777f484))
* **infra:** drop hooks original backup after a successful restore ([696b2e4](https://github.com/adammatthewsteinberger/cursorloop/commit/696b2e4032af5b41e96008711b351ef30cb85108))
* **infra:** record hooks restore metadata before mutating hooks.json ([1bbb0d5](https://github.com/adammatthewsteinberger/cursorloop/commit/1bbb0d515f8a941a9fbca3b4d8a581f54de803a8))
* **infra:** tick the stall watchdog while a turn stream is in flight ([4d13fb0](https://github.com/adammatthewsteinberger/cursorloop/commit/4d13fb0ea80b42e9acb95ccb1b613c19e4dc41d1))


### Documentation

* add FOSS community files, CODEOWNERS, and accurate status ([5649001](https://github.com/adammatthewsteinberger/cursorloop/commit/56490010fb199b05b90fc39ac5d973c496c3fd9d))
* capture cursorloop design and implementation plan ([8f652d8](https://github.com/adammatthewsteinberger/cursorloop/commit/8f652d8b56d99a5ed5b25d06c667a858c8719c7a))
* publish MkDocs site to GitHub Pages ([#3](https://github.com/adammatthewsteinberger/cursorloop/issues/3)) ([5403356](https://github.com/adammatthewsteinberger/cursorloop/commit/540335665a2754bca193cd165f20e98be6e0208f))
* publish MkDocs site to GitHub Pages ([#3](https://github.com/adammatthewsteinberger/cursorloop/issues/3)) ([c550c63](https://github.com/adammatthewsteinberger/cursorloop/commit/c550c63c3ff10067fe0428fde5611dbca6b4ef6d))

## [0.2.0](https://github.com/adammatthewsteinberger/cursorloop/compare/cursorloop-v0.1.0...cursorloop-v0.2.0) (2026-08-14)


### Features

* **application:** add the autonomous runner with probe-based recovery and fault handling ([ec978bf](https://github.com/adammatthewsteinberger/cursorloop/commit/ec978bf6a3f484e3cdc5c59825183bcbee0c7eb7))
* **application:** declare protocol ports, DTOs, and the port fakes ([b31523d](https://github.com/adammatthewsteinberger/cursorloop/commit/b31523d3695ecfaf1958da26a8b82a2b890bf8ab))
* complete Tasks 16–20 (CLI, doctor, system harness, M4/M5) ([#1](https://github.com/adammatthewsteinberger/cursorloop/issues/1)) ([51d237b](https://github.com/adammatthewsteinberger/cursorloop/commit/51d237b3c53c51f6a88a476265cac1a2833ab4ba))
* complete Tasks 16–20 (CLI, doctor, system harness, M4/M5) ([#1](https://github.com/adammatthewsteinberger/cursorloop/issues/1)) ([936df1e](https://github.com/adammatthewsteinberger/cursorloop/commit/936df1e8f3d8294210eacc69a3f2037e23eccc76))
* **domain:** add adaptive probe scheduling with credits backoff and window bounds ([64fbf33](https://github.com/adammatthewsteinberger/cursorloop/commit/64fbf33e1afd634a6ca976ce8b9eb80dba06ee42))
* **domain:** add budget ledger, model profiles, agent selectors, and hook policy ([5a40513](https://github.com/adammatthewsteinberger/cursorloop/commit/5a40513dd025e93dee6756b9e49b1510f0640c9c))
* **domain:** add CapacityState and Fault algebraic data types ([5fe6f9d](https://github.com/adammatthewsteinberger/cursorloop/commit/5fe6f9df3c5dd3ab44c273823b93870993a50b29))
* **domain:** add the pure run-loop state machine with capacity-outranks-verdict ordering ([83e671f](https://github.com/adammatthewsteinberger/cursorloop/commit/83e671f2ca19f0a418210786a41a577586a06141))
* **domain:** classify Cursor turn signals into capacity states and faults ([1d057b1](https://github.com/adammatthewsteinberger/cursorloop/commit/1d057b132b29aa52c73f13fc73aeb7c53db31ded))
* **domain:** detect completion via verdict block, marker fallback, and plan reconciliation ([3436c03](https://github.com/adammatthewsteinberger/cursorloop/commit/3436c038a424ead2d55775d7b759bf27aecebab1))
* **domain:** parse Retry-After and add configurable billing/rate-limit lexicons ([4b87be2](https://github.com/adammatthewsteinberger/cursorloop/commit/4b87be2acd56a2dd54b28d42ddd193b83b72c25e))
* **infra:** add logging, redaction, run state, locking, audit, and config adapters ([22af255](https://github.com/adammatthewsteinberger/cursorloop/commit/22af255d29e5c5b48d9272475c49d185dbf34b00))
* **infra:** add the Cursor agent gateway, capacity probe, stall watchdog, and catalogs ([25ead2f](https://github.com/adammatthewsteinberger/cursorloop/commit/25ead2f7fa508281527683eb86dac21a14c452d9))
* **infra:** build Cursor agent options from a single create/resume builder ([72405ee](https://github.com/adammatthewsteinberger/cursorloop/commit/72405eeff2e93e23798faa2c8f066ad5fe04f1bc))
* **infra:** manage .cursor/hooks.json autonomy fragment with hash-verified restore ([a36bba2](https://github.com/adammatthewsteinberger/cursorloop/commit/a36bba2a7d5cdb5887f1822555050d13a421a118))
* **infra:** translate Cursor SDK runs and errors into turn signals ([e28b7ce](https://github.com/adammatthewsteinberger/cursorloop/commit/e28b7ce71b0256e6eca2e1f15fd75d0292c50850))


### Bug Fixes

* **application:** cap send-path Busy retries with jittered backoff ([8236ae7](https://github.com/adammatthewsteinberger/cursorloop/commit/8236ae70af7e377de24ffb43750edabd21bf8fc3))
* **application:** jitter transient backoff and always release runner resources ([eae2fd3](https://github.com/adammatthewsteinberger/cursorloop/commit/eae2fd302a845ffbd3c54bde0a64b07747995b2a))
* **ci:** build TestPyPI from develop; PyPI stays release/main-only ([#6](https://github.com/adammatthewsteinberger/cursorloop/issues/6)) ([89c82cb](https://github.com/adammatthewsteinberger/cursorloop/commit/89c82cb641b3452288d549d15cff4b9c9a2f8334))
* **domain:** default turn cost to unknown and enforce wall-clock while waiting ([1f2aa12](https://github.com/adammatthewsteinberger/cursorloop/commit/1f2aa121aca956eae7f0a54573d1daf09db6707e))
* **domain:** never raise from parse_retry_after on nan or mixed-offset datetimes ([26b4eb1](https://github.com/adammatthewsteinberger/cursorloop/commit/26b4eb1d38a120c7863ed6fc9d8dd4a6b9f71ef1))
* **infra:** complete a recorded-but-unapplied hooks install on retry ([0c1d1ed](https://github.com/adammatthewsteinberger/cursorloop/commit/0c1d1ede399e96d0a6290b853ca562362777f484))
* **infra:** drop hooks original backup after a successful restore ([696b2e4](https://github.com/adammatthewsteinberger/cursorloop/commit/696b2e4032af5b41e96008711b351ef30cb85108))
* **infra:** record hooks restore metadata before mutating hooks.json ([1bbb0d5](https://github.com/adammatthewsteinberger/cursorloop/commit/1bbb0d515f8a941a9fbca3b4d8a581f54de803a8))
* **infra:** tick the stall watchdog while a turn stream is in flight ([4d13fb0](https://github.com/adammatthewsteinberger/cursorloop/commit/4d13fb0ea80b42e9acb95ccb1b613c19e4dc41d1))


### Documentation

* add FOSS community files, CODEOWNERS, and accurate status ([5649001](https://github.com/adammatthewsteinberger/cursorloop/commit/56490010fb199b05b90fc39ac5d973c496c3fd9d))
* capture cursorloop design and implementation plan ([8f652d8](https://github.com/adammatthewsteinberger/cursorloop/commit/8f652d8b56d99a5ed5b25d06c667a858c8719c7a))
* publish MkDocs site to GitHub Pages ([#3](https://github.com/adammatthewsteinberger/cursorloop/issues/3)) ([5403356](https://github.com/adammatthewsteinberger/cursorloop/commit/540335665a2754bca193cd165f20e98be6e0208f))

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
