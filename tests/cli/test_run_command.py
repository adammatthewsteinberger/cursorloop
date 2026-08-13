from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from cursorloop.cli.app import app

runner = CliRunner()


def _auth_failure_script(tmp_path: Path) -> Path:
    script = tmp_path / "auth.json"
    script.write_text(
        json.dumps(
            {
                "probes": [{"signals": {}}],
                "turns": [
                    {
                        "signals": {
                            "error_type": "AuthenticationError",
                            "error_message": "bad key",
                        },
                        "output_text": "",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return script


def test_run_help_documents_the_never_block_flags() -> None:
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    for flag in ("--turn-timeout", "--stall-timeout", "--max-wait", "--managed-hooks"):
        assert flag in result.stdout


def test_test_agent_gate_requires_both_env_vars(monkeypatch, tmp_path: Path) -> None:
    """A scripted agent must never be reachable by setting one variable —
    especially not by an env var leaking into a real user's shell."""
    script = tmp_path / "script.json"
    script.write_text('{"probes": [], "turns": []}')
    monkeypatch.setenv("CURSORLOOP_TEST_AGENT_SCRIPT", str(script))
    monkeypatch.delenv("CURSORLOOP_ALLOW_TEST_AGENT", raising=False)

    plan = tmp_path / "plan.md"
    plan.write_text("- [ ] do a thing\n")
    result = runner.invoke(app, ["run", "--plan", str(plan)])
    assert result.exit_code != 0
    assert "CURSORLOOP_ALLOW_TEST_AGENT" in result.stdout


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "cursorloop" in result.stdout


def test_authentication_failure_exits_3(monkeypatch, tmp_path: Path) -> None:
    plan = tmp_path / "plan.md"
    plan.write_text("- [ ] do a thing\n")
    monkeypatch.setenv("CURSORLOOP_ALLOW_TEST_AGENT", "1")
    monkeypatch.setenv("CURSORLOOP_TEST_AGENT_SCRIPT", str(_auth_failure_script(tmp_path)))
    result = runner.invoke(
        app, ["run", "--plan", str(plan), "--cwd", str(tmp_path), "--no-managed-hooks"]
    )
    assert result.exit_code == 3
