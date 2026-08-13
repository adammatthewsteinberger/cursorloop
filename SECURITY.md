# Security policy

## Why this matters more than usual

`cursorloop` is designed to drive a Cursor Agent **unattended**, which means it:

- Merges autonomy policy into `.cursor/hooks.json` for the duration of a run
  and restores it afterward (hash-verified; a mid-run user edit wins).
- Reads `CURSOR_API_KEY` and may surface credential-shaped strings in logs
  unless redaction holds (`infrastructure/redact.py` scrubbing `crsr_…` and
  known secret keys).
- Writes per-run audit/event JSONL under `.cursorloop/runs/<run_id>/` that can
  contain prompts, tool output, and error bodies — treat run dirs as sensitive.
- Edits the working tree and runs tools without waiting on a human.

The env vars `CURSORLOOP_ALLOW_TEST_AGENT` / `CURSORLOOP_TEST_AGENT_SCRIPT`
activate a JSON-scripted agent for tests only. Never set them on machines
running real work unless you intend the scripted harness.

## Supported versions

Only the latest released version receives security fixes. This project is
pre-1.0; there is no long-term-support branch.

## Reporting a vulnerability

Please **do not** open a public issue for security reports.

Email **adam@matthewsteinberger.com** with:

- A short description of the issue and impact
- Steps to reproduce (or a proof-of-concept)
- Affected version / commit if known

You should receive an acknowledgment within a few business days. We will
coordinate a fix and disclosure timeline with you.

## Preferential areas

Reports involving credential leakage, redaction gaps, hook restore failures
that leave elevated autonomy in place, or the test-agent gate being reachable
without both env vars are treated as high priority.
