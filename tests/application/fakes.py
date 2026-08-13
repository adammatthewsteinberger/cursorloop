"""Real fakes (not unittest.mock.Mock) implementing application/ports.py's
Protocols, so no test ever waits on a human or calls time.sleep() for real.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from cursorloop.application.dto import TurnOutcome
from cursorloop.domain.classify import TurnSignals
from cursorloop.domain.model_profile import ModelProfile

_DEFAULT_START = datetime(2026, 8, 13, 12, 0, tzinfo=UTC)


class FakeClock:
    """Settable, monotonic clock. Refuses to run backwards."""

    def __init__(self, start: datetime | None = None) -> None:
        self._now = start if start is not None else _DEFAULT_START

    def now(self) -> datetime:
        return self._now

    def advance_to(self, instant: datetime) -> None:
        if instant < self._now:
            raise ValueError("FakeClock is monotonic")
        self._now = instant


class FakeSleeper:
    """sleep_until() jumps the paired FakeClock to the target instant.

    Never calls a real sleep primitive — a simulated seven-day wait runs in
    microseconds of wall-clock time.
    """

    def __init__(self, clock: FakeClock) -> None:
        self._clock = clock
        self.total_simulated_seconds = 0.0
        self.real_sleep_calls = 0
        self.wait_log: list[datetime] = []

    async def sleep_until(self, instant: datetime) -> None:
        self.wait_log.append(instant)
        current = self._clock.now()
        delta = (instant - current).total_seconds()
        if delta <= 0:
            return
        self.total_simulated_seconds += delta
        self._clock.advance_to(instant)


class FakeAgentGateway:
    """Replays a scripted list of TurnOutcome, one per send_turn() call.

    Raises IndexError if more turns are requested than were scripted — a
    runaway loop should fail loudly, not hang.
    """

    def __init__(self, script: list[TurnOutcome], *, agent_id: str = "fake-agent") -> None:
        self._script = list(script)
        self._agent_id = agent_id
        self.sent_prompts: list[str] = []
        self.force_flags: list[bool] = []
        self.profiles: list[ModelProfile] = []
        self.cwds: list[str] = []
        self.closed = False
        self.cancel_calls = 0
        self.send_calls = 0

    async def send_turn(self, prompt_text: str, *, force: bool = False) -> TurnOutcome:
        self.sent_prompts.append(prompt_text)
        self.force_flags.append(force)
        self.send_calls += 1
        return self._script.pop(0)

    async def close(self) -> None:
        self.closed = True

    async def set_profile(self, profile: ModelProfile) -> None:
        self.profiles.append(profile)

    async def set_cwd(self, cwd: str) -> None:
        self.cwds.append(cwd)

    async def cancel_active_run(self) -> bool:
        self.cancel_calls += 1
        return True

    def agent_id(self) -> str:
        return self._agent_id


class FakeCapacityProbe:
    """Replays a scripted list of TurnSignals, one per probe() call."""

    def __init__(self, script: list[TurnSignals]) -> None:
        self._script = list(script)
        self.calls = 0

    async def probe(self) -> TurnOutcome:
        self.calls += 1
        signals = self._script.pop(0)
        return TurnOutcome(
            signals=signals,
            verdict=None,
            output_text="",
            cost_usd=None,
            cost_pending=True,
        )


class FakeHookManager:
    def __init__(self) -> None:
        self._installed = False
        self._restored_after_install = False

    def install(self) -> None:
        self._installed = True
        self._restored_after_install = False

    def restore(self) -> bool:
        if not self._installed:
            return False
        self._installed = False
        self._restored_after_install = True
        return True

    def is_installed(self) -> bool:
        return self._installed

    @property
    def installed_then_restored(self) -> bool:
        return self._restored_after_install


class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def notify(self, message: str) -> None:
        self.messages.append(message)


class FakeAuditLog:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append((event_type, payload))


class FakeRunStateStore:
    def __init__(self) -> None:
        self.saved: dict[str, dict[str, Any]] = {}

    def save(self, run_id: str, state: dict[str, Any]) -> None:
        self.saved[run_id] = dict(state)

    def load(self, run_id: str) -> dict[str, Any] | None:
        return self.saved.get(run_id)


class FakeAgentLock:
    def __init__(self) -> None:
        self.held: set[str] = set()

    def acquire(self, agent_id: str) -> bool:
        if agent_id in self.held:
            return False
        self.held.add(agent_id)
        return True

    def release(self, agent_id: str) -> None:
        self.held.discard(agent_id)


class FakeUsageReader:
    """``billed_cost_usd`` defaults to None — unknown, never zero."""

    def __init__(self, *, tokens: int = 0, billed_cost_usd: float | None = None) -> None:
        self._tokens = tokens
        self._billed_cost_usd = billed_cost_usd

    async def turn_tokens(self, run_id: str) -> int:
        del run_id
        return self._tokens

    async def billed_cost_usd(self) -> float | None:
        return self._billed_cost_usd
