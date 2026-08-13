from __future__ import annotations

from typer.testing import CliRunner

from cursorloop.cli.app import app

runner = CliRunner()


def test_cloud_help_marks_partial() -> None:
    result = runner.invoke(app, ["cloud", "--help"])
    assert result.exit_code == 0
    assert "PARTIAL" in result.stdout or "partial" in result.stdout.lower()


def test_cloud_status_explains_deferral() -> None:
    result = runner.invoke(app, ["cloud", "status"])
    assert result.exit_code == 0
    assert "ADR-0006" in result.stdout or "deferred" in result.stdout.lower()


def test_cloud_me_is_loud_partial() -> None:
    result = runner.invoke(app, ["cloud", "me"])
    assert result.exit_code == 0
    assert "getMe" in result.stdout
