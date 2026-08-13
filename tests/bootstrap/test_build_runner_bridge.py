from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from cursorloop.bootstrap import BuiltRunner, build_runner
from cursorloop.infrastructure.config import RunnerConfig


def test_build_runner_launches_bridge_when_no_client(tmp_path: Path) -> None:
    config = RunnerConfig(api_key="crsr_test", managed_hooks=False)
    fake_bridge = SimpleNamespace(
        client=object(),
        agent=SimpleNamespace(agent_id="a1", close=lambda: None),
        owns_client=True,
        close=lambda: None,
    )
    with (
        patch("cursorloop.bootstrap.open_live_bridge", return_value=fake_bridge) as open_bridge,
        patch("cursorloop.bootstrap.CursorAgentGateway") as gateway_cls,
        patch("cursorloop.bootstrap.CursorCapacityProbe"),
    ):
        gateway_cls.return_value = SimpleNamespace(
            agent_id=lambda: "a1",
            close=lambda: None,
            send_turn=None,
            set_profile=None,
            set_cwd=None,
            cancel_active_run=None,
        )
        built = build_runner(cwd=tmp_path, config=config)
    assert isinstance(built, BuiltRunner)
    open_bridge.assert_called_once()
    assert built.bridge is fake_bridge
    built.close()


def test_build_runner_uses_scripted_without_bridge(tmp_path: Path, monkeypatch: object) -> None:
    script = tmp_path / "done.json"
    script.write_text(
        json_dumps_done(),
        encoding="utf-8",
    )
    monkeypatch.setenv("CURSORLOOP_ALLOW_TEST_AGENT", "1")  # type: ignore[attr-defined]
    monkeypatch.setenv("CURSORLOOP_TEST_AGENT_SCRIPT", str(script))  # type: ignore[attr-defined]
    config = RunnerConfig(managed_hooks=False)
    with patch("cursorloop.bootstrap.open_live_bridge") as open_bridge:
        built = build_runner(cwd=tmp_path, config=config)
    open_bridge.assert_not_called()
    assert built.bridge is None
    built.close()


def json_dumps_done() -> str:
    return """{
  "probes": [{"signals": {}}],
  "turns": [{
    "signals": {},
    "verdict": {"complete": true, "remaining_work": [], "blocked_on": null, "summary": "done"},
    "output_text": "CURSORLOOP_TASK_FULLY_COMPLETE"
  }]
}
"""
