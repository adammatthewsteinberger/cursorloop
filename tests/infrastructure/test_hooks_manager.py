# tests/infrastructure/test_hooks_manager.py
import json
import stat
import subprocess
from pathlib import Path

from cursorloop.domain.autonomy import autonomy_preamble
from cursorloop.domain.hooks_policy import (
    MANAGED_EVENTS,
    allow_payload,
    preamble_injection_payload,
)
from cursorloop.infrastructure.agent.hooks import ManagedHooks


def test_install_appends_and_never_replaces_existing_entries(tmp_path: Path) -> None:
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    hooks_file.write_text(
        json.dumps({"version": 1, "hooks": {"afterFileEdit": [{"command": "./fmt.sh"}]}})
    )

    ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop").install()

    merged = json.loads(hooks_file.read_text())
    assert {"command": "./fmt.sh"} in merged["hooks"]["afterFileEdit"]
    assert merged["hooks"]["preToolUse"]


def test_restore_returns_the_original_bytes_exactly(tmp_path: Path) -> None:
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    original = json.dumps({"version": 1, "hooks": {"afterFileEdit": [{"command": "./fmt.sh"}]}})
    hooks_file.write_text(original)

    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()
    assert manager.restore() is True
    assert hooks_file.read_text() == original


def test_a_user_edit_during_the_run_wins_and_restore_declines(tmp_path: Path) -> None:
    """We hash what we wrote. If the on-disk bytes changed, the user edited the
    file mid-run — their edit wins, we log loudly and leave it alone."""
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    hooks_file.write_text(json.dumps({"version": 1, "hooks": {}}))

    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()
    hooks_file.write_text(json.dumps({"version": 1, "hooks": {"stop": [{"command": "./mine.sh"}]}}))

    assert manager.restore() is False
    assert "mine.sh" in hooks_file.read_text()


def test_install_when_no_hooks_file_exists_creates_one_and_removes_it_on_restore(
    tmp_path: Path,
) -> None:
    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()
    assert (tmp_path / ".cursor" / "hooks.json").exists()
    assert manager.restore() is True
    assert not (tmp_path / ".cursor" / "hooks.json").exists()


def test_generated_scripts_never_exit_2(tmp_path: Path) -> None:
    """Exit 2 blocks the action. cursorloop's hooks exist to ALLOW, so none of
    our scripts may ever use it — and any other non-zero exit fails open,
    which is the correct failure direction for autonomy."""
    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()
    for script in (tmp_path / ".cursorloop" / "hooks").glob("*.sh"):
        assert "exit 2" not in script.read_text()


def test_install_records_hash_state_and_is_installed(tmp_path: Path) -> None:
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    hooks_file.write_text(json.dumps({"version": 1, "hooks": {}}))

    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    assert manager.is_installed() is False
    manager.install()
    assert manager.is_installed() is True

    state = json.loads((tmp_path / ".cursorloop" / "state.json").read_text())
    assert state["hooks_existed"] is True
    assert state["hooks_original_path"]
    assert len(state["hooks_original_sha256"]) == 64
    assert len(state["hooks_merged_sha256"]) == 64
    assert state["hooks_original_sha256"] != state["hooks_merged_sha256"]

    assert manager.restore() is True
    assert manager.is_installed() is False


def test_generated_scripts_are_owner_only_posix_and_emit_allow(
    tmp_path: Path,
) -> None:
    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()

    scripts = list((tmp_path / ".cursorloop" / "hooks").glob("*.sh"))
    names = {path.name for path in scripts}
    assert names == {f"{event}.sh" for event in MANAGED_EVENTS}

    for script in scripts:
        mode = stat.S_IMODE(script.stat().st_mode)
        assert mode == 0o700
        assert not (mode & (stat.S_IWGRP | stat.S_IWOTH | stat.S_IROTH | stat.S_IXOTH))
        text = script.read_text()
        assert text.startswith("#!/bin/sh")
        assert "exit 0" in text
        assert "exit 2" not in text

        completed = subprocess.run(  # noqa: S603 - argv only, generated script
            [str(script)],
            check=False,
            capture_output=True,
            input=b'{"probe":true}',
        )
        assert completed.returncode == 0
        payload = json.loads(completed.stdout.decode())
        event = script.stem
        if event == "beforeSubmitPrompt":
            assert payload == preamble_injection_payload(autonomy_preamble())
        elif event == "stop":
            assert payload.get("permission", "allow") != "deny"
            captured = tmp_path / ".cursorloop" / "stop-final.txt"
            assert captured.read_bytes() == b'{"probe":true}'
        else:
            assert payload == allow_payload(event)


def test_install_appends_to_an_existing_managed_event_array(tmp_path: Path) -> None:
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    hooks_file.write_text(
        json.dumps({"version": 1, "hooks": {"preToolUse": [{"command": "./mine.sh"}]}})
    )

    ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop").install()

    merged = json.loads(hooks_file.read_text())
    assert merged["hooks"]["preToolUse"][0] == {"command": "./mine.sh"}
    assert len(merged["hooks"]["preToolUse"]) >= 2


def test_install_is_idempotent(tmp_path: Path) -> None:
    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    manager.install()
    first = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
    manager.install()
    second = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
    assert first == second


def test_restore_without_install_returns_false(tmp_path: Path) -> None:
    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    assert manager.restore() is False


def test_install_updates_existing_state_json_without_dropping_other_keys(
    tmp_path: Path,
) -> None:
    state_dir = tmp_path / ".cursorloop"
    state_dir.mkdir()
    (state_dir / "state.json").write_text(json.dumps({"run_id": "abc"}))

    manager = ManagedHooks(workspace=tmp_path, state_dir=state_dir)
    manager.install()
    state = json.loads((state_dir / "state.json").read_text())
    assert state["run_id"] == "abc"
    assert "hooks_merged_sha256" in state

    assert manager.restore() is True
    leftover = json.loads((state_dir / "state.json").read_text())
    assert leftover == {"run_id": "abc"}


def test_diff_describes_the_fragment_that_would_be_appended(tmp_path: Path) -> None:
    hooks_file = tmp_path / ".cursor" / "hooks.json"
    hooks_file.parent.mkdir(parents=True)
    hooks_file.write_text(
        json.dumps({"version": 1, "hooks": {"afterFileEdit": [{"command": "./fmt.sh"}]}})
    )

    manager = ManagedHooks(workspace=tmp_path, state_dir=tmp_path / ".cursorloop")
    shown = manager.diff()
    assert "preToolUse" in shown
    assert "./fmt.sh" in shown or "afterFileEdit" in shown
