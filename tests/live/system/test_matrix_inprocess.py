from __future__ import annotations

import pytest

pytestmark = pytest.mark.system


def test_happy_path_completes(system_env) -> None:
    result = system_env.run(script="done.json")
    assert result.exit_code == 0
    assert system_env.hooks_restored()
    events = system_env.audit_events()
    assert any(e.get("event_type") == "finished" for e in events)


def test_credits_exhaustion_then_top_up_resumes_with_real_adapters(system_env) -> None:
    """Real FS/control/audit adapters + scripted agent + FakeClock.

    End-to-end proof of the founding invariant: credits exhaustion probes
    (never deadline-sleeps), recovers when capacity returns, spends no wall clock.
    """
    result = system_env.run(script="credits_then_available.json")
    assert result.exit_code == 0
    events = system_env.audit_events()
    assert any(e.get("event_type") == "entered_credits_exhausted" for e in events)
    assert any(e.get("event_type") == "capacity_restored" for e in events)
    assert system_env.sleeper.real_sleep_calls == 0


def test_stop_mid_wait_drains_gracefully_and_exits_130(system_env) -> None:
    result = system_env.run(script="window_far_future.json", stop_after_seconds=1)
    assert result.exit_code == 130
    assert system_env.state()["phase"] == "WAITING"
    assert system_env.hooks_restored() is True


def test_max_wait_exceeded_exits_4_with_a_named_reason(system_env) -> None:
    result = system_env.run(script="window_far_future.json", max_wait="60s")
    assert result.exit_code == 4
    assert "max wait exceeded" in result.stdout


def test_resume_after_stall(system_env) -> None:
    result = system_env.run(script="stall_then_recover.json")
    assert result.exit_code == 0
