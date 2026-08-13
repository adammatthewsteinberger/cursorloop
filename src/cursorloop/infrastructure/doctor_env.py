"""Doctor findings — environment checks for unattended readiness."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class Finding:
    name: str
    level: Literal["pass", "warn", "fail"]
    detail: str
    remedy: str = ""


def _mcp_servers(workspace: Path) -> dict[str, Any]:
    path = workspace / ".cursor" / "mcp.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    servers = data.get("mcpServers", {})
    return servers if isinstance(servers, dict) else {}


def _needs_oauth(config: object) -> bool:
    if not isinstance(config, dict):
        return False
    return bool("url" in config and "command" not in config)


def _safe_detail(name: str, config: dict[str, Any]) -> str:
    kind = "url" if "url" in config else "command"
    return f"MCP server {name!r} ({kind}) needs a saved OAuth login for unattended runs"


def check_mcp_oauth_readiness(
    *,
    workspace: Path,
    saved_logins: frozenset[str],
    is_service_account: bool = False,
) -> list[Finding]:
    """Fail when a remote MCP server has no saved login the SDK can reuse."""
    findings: list[Finding] = []
    servers = _mcp_servers(workspace)
    for name, config in servers.items():
        if not isinstance(config, dict):
            continue
        # Never echo env/headers — only structural detail.
        if is_service_account and _needs_oauth(config):
            findings.append(
                Finding(
                    name=f"mcp-oauth:{name}",
                    level="fail",
                    detail=(
                        f"Service-account keys cannot fall back to user auth for "
                        f"MCP server {name!r}"
                    ),
                    remedy="Use a user API key with a saved MCP login, or remove the server.",
                )
            )
            continue
        if _needs_oauth(config) and name not in saved_logins:
            findings.append(
                Finding(
                    name=f"mcp-oauth:{name}",
                    level="fail",
                    detail=_safe_detail(name, config),
                    remedy=f"Open Cursor, sign in to MCP server {name!r}, then re-run doctor.",
                )
            )
        elif "command" in config:
            findings.append(
                Finding(
                    name=f"mcp-local:{name}",
                    level="pass",
                    detail=f"MCP server {name!r} uses a local command (no OAuth browser flow).",
                )
            )
    return findings


def check_api_key_present(api_key: str | None) -> Finding:
    if api_key:
        return Finding(name="cursor-api-key", level="pass", detail="CURSOR_API_KEY is set")
    return Finding(
        name="cursor-api-key",
        level="fail",
        detail="CURSOR_API_KEY is unset",
        remedy="Export CURSOR_API_KEY from the Cursor dashboard.",
    )


def check_cursorloop_gitignored(workspace: Path) -> Finding:
    gitignore = workspace / ".gitignore"
    if not gitignore.is_file():
        return Finding(
            name="cursorloop-gitignore",
            level="warn",
            detail="No .gitignore; .cursorloop/ may be committed",
            remedy="Add '.cursorloop/' to .gitignore",
        )
    text = gitignore.read_text(encoding="utf-8")
    if ".cursorloop" in text:
        return Finding(
            name="cursorloop-gitignore",
            level="pass",
            detail=".cursorloop/ appears in .gitignore",
        )
    return Finding(
        name="cursorloop-gitignore",
        level="fail",
        detail=".cursorloop/ is not git-ignored",
        remedy="Add '.cursorloop/' to .gitignore (run state holds prompts/transcripts).",
    )


def run_doctor(
    *,
    workspace: Path,
    saved_logins: frozenset[str] = frozenset(),
    is_service_account: bool = False,
    api_key: str | None = None,
) -> list[Finding]:
    findings: list[Finding] = [
        check_api_key_present(api_key if api_key is not None else os.environ.get("CURSOR_API_KEY")),
        check_cursorloop_gitignored(workspace),
    ]
    findings.extend(
        check_mcp_oauth_readiness(
            workspace=workspace,
            saved_logins=saved_logins,
            is_service_account=is_service_account,
        )
    )
    return findings


def findings_as_json(findings: list[Finding]) -> str:
    return json.dumps([asdict(f) for f in findings], indent=2) + "\n"
