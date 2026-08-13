from __future__ import annotations

from pathlib import Path

import typer

from cursorloop.application.usecases.doctor import explain_error_payload
from cursorloop.infrastructure.doctor_env import findings_as_json, run_doctor


def doctor(
    cwd_dir: Path | None = typer.Option(None, "--cwd", exists=True, file_okay=False),
    as_json: bool = typer.Option(False, "--json", help="Emit findings as JSON"),
    explain_error: Path | None = typer.Option(
        None,
        "--explain-error",
        exists=True,
        readable=True,
        help="Classify a captured error payload offline",
    ),
) -> None:
    """Fail-fast preflight checks before a multi-hour unattended run."""
    if explain_error is not None:
        try:
            name = explain_error_payload(explain_error)
        except (OSError, ValueError, TypeError) as exc:
            typer.echo(f"Could not classify payload: {exc}", err=True)
            raise typer.Exit(code=1) from exc
        typer.echo(name)
        raise typer.Exit(code=0)

    cwd = cwd_dir.resolve() if cwd_dir is not None else Path.cwd()
    findings = run_doctor(workspace=cwd)
    if as_json:
        typer.echo(findings_as_json(findings), nl=False)
    else:
        for finding in findings:
            typer.echo(f"[{finding.level}] {finding.name}: {finding.detail}")
            if finding.remedy:
                typer.echo(f"  remedy: {finding.remedy}")
    if any(f.level == "fail" for f in findings):
        raise typer.Exit(code=1)
