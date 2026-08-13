"""Own the Cursor SDK bridge lifetime and create/resume durable agents.

``bootstrap`` calls this module so ``cursor_sdk`` stays inside infrastructure/
while the composition root still owns when the bridge starts and stops.
"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cursor_sdk import Agent, CursorClient

from cursorloop.domain.model_profile import ModelProfile
from cursorloop.infrastructure.agent.options import build_agent_options

LaunchBridge = Callable[..., Any]
_API_KEY_ENV = "CURSOR_API_KEY"


@dataclass(frozen=True, slots=True)
class LiveBridge:
    """Bridge client + durable agent created for one autonomous run."""

    client: Any
    agent: Any
    owns_client: bool = True

    def close(self) -> None:
        """Release resources.

        Agent close is primarily owned by ``CursorAgentGateway.close`` (runner
        ``finally``). This method still attempts agent close for callers that
        never entered the runner, but suppresses already-gone agents so the
        CLI ``built.close()`` path cannot crash after a successful turn.
        """
        closer = getattr(self.agent, "close", None)
        if callable(closer):
            with contextlib.suppress(Exception):
                closer()
        if self.owns_client:
            shutdown = getattr(self.client, "close", None)
            if callable(shutdown):
                with contextlib.suppress(Exception):
                    shutdown()


def launch_bridge_client(
    workspace: Path,
    *,
    api_key: str | None = None,
    launch_bridge: LaunchBridge | None = None,
) -> Any:
    """Start ``CursorClient.launch_bridge`` for ``workspace``.

    The SDK's ``launch_bridge`` does not accept an auth kwarg — it constructs
    ``CursorClient`` with ``allow_api_key_env_fallback=True`` and reads
    ``CURSOR_API_KEY``. When a key is supplied explicitly, export it into the
    process env before launching so the bridge can authenticate.
    """
    if api_key:
        os.environ[_API_KEY_ENV] = api_key
    launcher = launch_bridge if launch_bridge is not None else CursorClient.launch_bridge
    return launcher(workspace=str(workspace), allow_api_key_env_fallback=True)


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
    create_kwargs: dict[str, Any] = {"options": options, "client": live_client}
    if api_key:
        create_kwargs["api_key"] = api_key
    if resume_agent_id:
        agent = resume(resume_agent_id, options=options, client=live_client)
    else:
        agent = create(**create_kwargs)
    return LiveBridge(client=live_client, agent=agent, owns_client=owns_client)
