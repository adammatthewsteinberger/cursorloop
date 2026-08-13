"""Bind OpenAPI operations to Typer commands (sketch — partial surface)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import typer

from cursorloop.infrastructure.api.registry import DEFERRED_REASON, PARTIAL_OPERATIONS


@dataclass(frozen=True, slots=True)
class BoundOperation:
    operation_id: str
    summary: str
    handler: Callable[..., None]


def bind_partial_commands(app: typer.Typer) -> list[BoundOperation]:
    """Register explicitly partial commands; refuse undeclared operations."""
    bound: list[BoundOperation] = []

    @app.command("me")
    def me() -> None:
        """GET /v1/me — partial sketch."""
        typer.echo(f"getMe: {DEFERRED_REASON}")

    @app.command("models")
    def models() -> None:
        """GET /v1/models — partial sketch."""
        typer.echo(f"listModels: {DEFERRED_REASON}")

    @app.command("create")
    def create() -> None:
        """POST /v1/agents — partial sketch."""
        typer.echo(f"createAgent: {DEFERRED_REASON}")

    @app.command("get")
    def get(agent_id: str = typer.Argument(..., help="Cloud agent id")) -> None:
        """GET /v1/agents/{id} — partial sketch."""
        typer.echo(f"getAgent({agent_id}): {DEFERRED_REASON}")

    @app.command("cancel")
    def cancel(agent_id: str = typer.Argument(..., help="Cloud agent id")) -> None:
        """POST /v1/agents/{id}/cancel — partial sketch."""
        typer.echo(f"cancelAgent({agent_id}): {DEFERRED_REASON}")

    bound.extend(
        [
            BoundOperation("getMe", "Current authenticated identity", me),
            BoundOperation("listModels", "List available models", models),
            BoundOperation("createAgent", "Create a cloud agent", create),
            BoundOperation("getAgent", "Get a cloud agent by id", get),
            BoundOperation("cancelAgent", "Cancel a running cloud agent", cancel),
        ]
    )
    missing = PARTIAL_OPERATIONS - {b.operation_id for b in bound}
    if missing:
        raise RuntimeError(f"partial binder missing operations: {sorted(missing)}")
    return bound


def operation_to_click_name(operation_id: str) -> str:
    """Map camelCase operationId to a kebab CLI name (sketch helper)."""
    chars: list[str] = []
    for i, ch in enumerate(operation_id):
        if ch.isupper() and i > 0:
            chars.append("-")
        chars.append(ch.lower())
    return "".join(chars)


def json_body_option_help() -> dict[str, Any]:
    return {
        "--json": "Inline JSON body",
        "--json-file": "Path to JSON body (@path inlining supported later)",
    }
