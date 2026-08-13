"""Notifier — loud stderr banner when a human must act (e.g. credits)."""

from __future__ import annotations

import sys


class StderrNotifier:
    def notify(self, message: str) -> None:
        bar = "!" * min(78, max(20, len(message)))
        print(bar, file=sys.stderr)
        print(message, file=sys.stderr)
        print(bar, file=sys.stderr)
