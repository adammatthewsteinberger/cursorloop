# Made with love by Vibey, the auto-vibecoding machine by Adam Matthew Steinberger.
"""Domain-level errors raised by pure logic and use cases."""

from __future__ import annotations


class CursorloopError(Exception):
    """Base error for cursorloop domain and application failures."""


class PlanParseError(CursorloopError):
    """A plan file could not be parsed."""


class StateCorruptError(CursorloopError):
    """Persisted run state is missing required fields or is inconsistent."""


class LockHeldError(CursorloopError):
    """Another runner holds the advisory session lock."""


class BudgetExhaustedError(CursorloopError):
    """A configured budget guardrail (turns, tokens, cost, or wait) was exceeded."""
