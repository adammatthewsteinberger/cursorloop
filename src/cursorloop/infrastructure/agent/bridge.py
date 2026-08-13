"""Own the Cursor SDK bridge lifetime and create/resume durable agents.

``bootstrap`` calls this module so ``cursor_sdk`` stays inside infrastructure/
while the composition root still owns when the bridge starts and stops.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cursor_sdk import Agent, CursorClient

from cursorloop.domain.model_profile import ModelProfile
from cursorloop.infrastructure.agent.options import build_agent_options

LaunchBridge = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class LiveBridge:
    """Bridge client + durable agent created for one autonomous run."""

    client: Any
    agent: Any
    owns_client: bool = True

    def close(self) -> None:
        closer = getattr(self.agent, "close", None)
        if callable(closer):
            closer()
        if self.owns_client:
            shutdown = getattr(self.client, "close", None)
            if callable(shutdown):
                shutdown()


def launch_bridge_client(
    workspace: Path,
    *,
    api_key: str | None = None,
    launch_bridge: LaunchBridge | None = None,
) -> Any:
    """Start ``CursorClient.launch_bridge`` for ``workspace``.

    Passes ``auth_token`` when an API key is available; otherwise the SDK may
    fall back to ``CURSOR_API_KEY`` when allowed.
    """
    launcher = launch_bridge if launch_bridge is not None else CursorClient.launch_bridge
    kwargs: dict[str, Any] = {"workspace": str(workspace)}
    if api_key:
        kwargs["auth_token"] = api_key
    return launcher(**kwargs)


def open_live_bridge(
    *,
    workspace: Path,
    profile: ModelProfile,
    api_key: str | None = None,
    resume_agent_id: str | None = None,
    client: Any | None = None,
    launch_bridge: LaunchBridge | None = None,
    create_agent: Callable[..., Any] | None = None,
    resume_agent: Callable[..., Any] | None = None,
) -> LiveBridge:
    """Launch (or reuse) a bridge client and create/resume a durable Agent."""
    owns_client = client is None
    live_client = (
        client
        if client is not None
        else launch_bridge_client(workspace, api_key=api_key, launch_bridge=launch_bridge)
    )
    options = build_agent_options(profile=profile, cwd=str(workspace))
    create = create_agent if create_agent is not None else Agent.create
    resume = resume_agent if resume_agent is not None else Agent.resume
    if resume_agent_id:
        agent = resume(resume_agent_id, options=options, client=live_client)
    else:
        agent = create(options=options, client=live_client)
    return LiveBridge(client=live_client, agent=agent, owns_client=owns_client)
