# Made with ❤️ by [Vibey](https://adammatthewsteinberger.github.io/vibey/), Developed by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com/) ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger/)).
# Made with love by Vibey, the auto-vibecoding machine by Adam Matthew Steinberger.
from __future__ import annotations

from cursorloop.infrastructure.stream_ui import StreamUiApp


def test_stream_ui_collects_deltas_and_steps() -> None:
    ui = StreamUiApp()
    ui.on_delta("hello")
    ui.on_step({"phase": "RUNNING"})
    assert ui.deltas == ["hello"]
    assert ui.steps[0]["phase"] == "RUNNING"
