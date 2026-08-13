# Cloud Agents REST surface — documented deferral (M4 sketch)

- Status: Accepted
- Date: 2026-08-13
- Deciders: cursorloop maintainers

## Context

The Cloud Agents API v1 is beta and warned to change. Generating a full
`cursorloop cloud …` / `cursorloop api …` surface from an unstable published
OpenAPI document would either (a) break between releases or (b) ship a
hand-written partial CLI that looks complete.

M1–M3 (local autonomous runner) do not depend on Cloud Agents REST.

## Decision

**Defer full OpenAPI → CLI generation.** Ship a digest-pinned *sketch*
document covering only the runner-needed subset:

- `GET /v1/me`
- `GET /v1/models`
- agent create / get / cancel (and delete listed for drift completeness)

Commands under `cursorloop cloud` are **explicitly labelled PARTIAL** and
print the deferral reason rather than pretending to be a complete binder.
CI pins the vendored sketch digest and asserts every `operationId` is
registered so silent removals fail. A scheduled workflow re-fetches the
published vendor document when a URL is configured and fails on digest drift.

## Consequences

- Operators cannot mistake a stub for a full Cloud Agents CLI.
- Regenerating a complete surface later is a deliberate digest bump + ADR
  amendment, not a silent expansion.
- Local autonomous runs remain unaffected.
