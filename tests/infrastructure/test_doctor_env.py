from __future__ import annotations

from pathlib import Path

from cursorloop.infrastructure.doctor_env import check_mcp_oauth_readiness


def test_an_mcp_server_needing_oauth_is_a_fatal_finding(tmp_path: Path) -> None:
    """The SDK can reuse a login saved by the Cursor app but cannot open a
    browser to sign you in. Discovering this mid-run is how an unattended run
    dies at 3am; discovering it in doctor is how it doesn't."""
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".cursor" / "mcp.json").write_text(
        '{"mcpServers": {"linear": {"url": "https://mcp.linear.app/mcp"}}}'
    )
    findings = check_mcp_oauth_readiness(workspace=tmp_path, saved_logins=frozenset())
    assert [f.name for f in findings if f.level == "fail"] == ["mcp-oauth:linear"]


def test_a_saved_login_clears_the_finding(tmp_path: Path) -> None:
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".cursor" / "mcp.json").write_text(
        '{"mcpServers": {"linear": {"url": "https://mcp.linear.app/mcp"}}}'
    )
    findings = check_mcp_oauth_readiness(workspace=tmp_path, saved_logins=frozenset({"linear"}))
    assert all(f.level != "fail" for f in findings)


def test_service_account_keys_cannot_fall_back_to_user_auth(tmp_path: Path) -> None:
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".cursor" / "mcp.json").write_text(
        '{"mcpServers": {"linear": {"url": "https://mcp.linear.app/mcp"}}}'
    )
    findings = check_mcp_oauth_readiness(
        workspace=tmp_path, saved_logins=frozenset({"linear"}), is_service_account=True
    )
    assert any(f.level == "fail" for f in findings)


def test_doctor_never_prints_mcp_env_or_headers(tmp_path: Path) -> None:
    (tmp_path / ".cursor").mkdir()
    (tmp_path / ".cursor" / "mcp.json").write_text(
        '{"mcpServers": {"gh": {"command": "npx", "env": {"GITHUB_TOKEN": "ghp_secret"}}}}'
    )
    rendered = "\n".join(
        f.detail for f in check_mcp_oauth_readiness(workspace=tmp_path, saved_logins=frozenset())
    )
    assert "ghp_secret" not in rendered
