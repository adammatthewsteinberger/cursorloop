from __future__ import annotations

import pytest

from cursorloop.domain.control import (
    ControlCommand,
    Prompt,
    SavePoint,
    SetCwd,
    SetEffort,
    SetModel,
    Snapshot,
    Stop,
)


def test_control_command_union_covers_the_seven_variants() -> None:
    commands: list[ControlCommand] = [
        Stop(),
        Prompt(text="continue with the next item"),
        SetModel(model="composer-2.5"),
        SetEffort(effort="high"),
        SetCwd(path="/tmp/work"),
        Snapshot(),
        SavePoint(),
    ]
    assert [type(c).__name__ for c in commands] == [
        "Stop",
        "Prompt",
        "SetModel",
        "SetEffort",
        "SetCwd",
        "Snapshot",
        "SavePoint",
    ]


def test_blank_prompt_model_effort_and_cwd_are_rejected() -> None:
    with pytest.raises(ValueError, match="prompt"):
        Prompt(text="   ")
    with pytest.raises(ValueError, match="model"):
        SetModel(model="")
    with pytest.raises(ValueError, match="effort"):
        SetEffort(effort=" ")
    with pytest.raises(ValueError, match="cwd"):
        SetCwd(path="")
