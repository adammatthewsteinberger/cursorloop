"""The out-of-band control plane: commands an operator drops for a live run."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cursorloop.domain.control import ControlCommand


@runtime_checkable
class RunControl(Protocol):
    """Mid-run operator commands drained from the control-plane inbox."""

    def poll(self) -> list[ControlCommand]: ...
