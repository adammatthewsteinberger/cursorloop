"""Application ports — Protocols implemented by infrastructure/, never imported
from it. Each docstring states the shape contract, never a concrete type.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol, runtime_checkable

from cursorloop.application.dto import TurnOutcome
from cursorloop.domain.control import ControlCommand
from cursorloop.domain.model_profile import ModelProfile
from cursorloop.domain.session import AgentRef


@runtime_checkable
class Clock(Protocol):
    """Current instant as an aware datetime."""

    def now(self) -> datetime: ...


@runtime_checkable
class Sleeper(Protocol):
    """Wait until the given instant. Must not require a human."""

    async def sleep_until(self, instant: datetime) -> None: ...


@runtime_checkable
class AgentGateway(Protocol):
    """Wraps a durable cursor_sdk Agent. Each send_turn() maps to one
    agent.send() → Run. An errored Run does NOT invalidate the agent, so the
    outer loop is repeated sends on one handle, never respawn-and-reattach."""

    async def send_turn(self, prompt_text: str, *, force: bool = False) -> TurnOutcome: ...
    async def close(self) -> None: ...
    async def set_profile(self, profile: ModelProfile) -> None: ...
    async def set_cwd(self, cwd: str) -> None: ...
    async def cancel_active_run(self) -> bool: ...
    def agent_id(self) -> str: ...


@runtime_checkable
class CapacityProbe(Protocol):
    """Cheap throwaway capacity check. Returns turn signals, not a live-session turn."""

    async def probe(self) -> TurnOutcome: ...


@runtime_checkable
class AgentCatalog(Protocol):
    """Resolved agent handles for a working directory. Never a filesystem glob."""

    def most_recent(self, cwd: str) -> AgentRef | None: ...
    def list_all(self, cwd: str | None = None) -> list[AgentRef]: ...


@runtime_checkable
class ModelCatalog(Protocol):
    """Vendor-published model identifiers. Implementations return ids, never SDK types."""

    def list_all(self) -> list[str]: ...


@runtime_checkable
class UsageReader(Protocol):
    """Per-turn tokens and billed dollars. ``billed_cost_usd`` is None when unknown."""

    async def turn_tokens(self, run_id: str) -> int: ...
    async def billed_cost_usd(self) -> float | None: ...


@runtime_checkable
class HookManager(Protocol):
    """Autonomy policy lives in .cursor/hooks.json because Cursor hooks are
    file-based only — there is no programmatic permission callback."""

    def install(self) -> None: ...
    def restore(self) -> bool: ...
    def is_installed(self) -> bool: ...


@runtime_checkable
class ProgressReporter(Protocol):
    """Operator-visible progress: a turn was sent, a wait began, or the run ended."""

    def turn_sent(self, *, attempt: int) -> None: ...
    def waiting(self, *, reason: str, until: datetime) -> None: ...
    def finished(self, *, success: bool, reason: str) -> None: ...


@runtime_checkable
class AuditLog(Protocol):
    """Append-only structured events for a single run."""

    def record(self, event_type: str, payload: dict[str, Any]) -> None: ...


@runtime_checkable
class Notifier(Protocol):
    """Fire-and-forget operator alert. Used when a human must act (credits)."""

    def notify(self, message: str) -> None: ...


@runtime_checkable
class Logger(Protocol):
    """Structured event log. bind() returns a child logger with extra context."""

    def bind(self, **kwargs: Any) -> Logger: ...
    def debug(self, event: str, **kwargs: Any) -> None: ...
    def info(self, event: str, **kwargs: Any) -> None: ...
    def warning(self, event: str, **kwargs: Any) -> None: ...
    def error(self, event: str, **kwargs: Any) -> None: ...


@runtime_checkable
class RunStateStore(Protocol):
    """Persisted run dicts keyed by run id. load returns None when absent."""

    def save(self, run_id: str, state: dict[str, Any]) -> None: ...
    def load(self, run_id: str) -> dict[str, Any] | None: ...


@runtime_checkable
class AgentLock(Protocol):
    """Advisory exclusive lock keyed by agent id."""

    def acquire(self, agent_id: str) -> bool: ...
    def release(self, agent_id: str) -> None: ...


@runtime_checkable
class RunControl(Protocol):
    """Mid-run operator commands drained from the control-plane inbox."""

    def poll(self) -> list[ControlCommand]: ...


@runtime_checkable
class RunEventSink(Protocol):
    """Structured run events for watchers. bind() sets the ambient context."""

    def emit(self, event_type: str, payload: dict[str, Any] | None = None) -> None: ...
    def bind(
        self,
        *,
        agent_id: str | None = None,
        attempt: int | None = None,
        phase: str | None = None,
        trace_id: str | None = None,
        turn_id: str | None = None,
    ) -> None: ...


@runtime_checkable
class StreamUi(Protocol):
    """Optional full-screen stream view fed token deltas and turn boundaries."""

    def on_delta(self, text: str, *, turn_id: str, seq: int) -> None: ...
    def on_turn_boundary(self, *, turn_id: str, attempt: int) -> None: ...
    def on_prompt(self, text: str) -> None: ...
    def on_assistant(self, text: str) -> None: ...
    def on_tool(self, name: str, summary: str) -> None: ...
    def on_status(self, state: dict[str, Any]) -> None: ...
    def close(self) -> None: ...


@runtime_checkable
class SavePointStore(Protocol):
    """Worktree save points. Refs are opaque objects until domain savepoint types land."""

    def create(
        self,
        *,
        run_id: str,
        label: str,
        message: str = "",
        attempt: int | None = None,
        verdict_name: str = "Continue",
        summary: str = "",
        remaining_work: tuple[str, ...] = (),
    ) -> object | None: ...
    def list_points(self, run_id: str) -> list[object]: ...
    def unwind(self, *, run_id: str, to: str, backup: bool) -> object: ...
    def changes_since(self, since_sha: str | None) -> str: ...


@runtime_checkable
class StateBus(Protocol):
    """Publish run state changes for external pollers / subscribers."""

    def publish(self, event_type: str, state: dict[str, Any]) -> None: ...


@runtime_checkable
class RunSnapshotSink(Protocol):
    """Write a handoff snapshot and publish its path and digest."""

    def emit(
        self,
        reason: str,
        *,
        context: dict[str, Any] | None = None,
        bundle: bool | None = None,
    ) -> object | None: ...


@runtime_checkable
class ApiGateway(Protocol):
    """Opaque vendor HTTP operations, keyed by method path."""

    def invoke(self, method_path: str, **kwargs: Any) -> Any: ...
