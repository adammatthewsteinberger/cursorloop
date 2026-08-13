"""Throwaway capacity probe: Agent.prompt with no tools and no transcript.

``tools=[]`` offers no built-in tools — the model can only respond with text.
``setting_sources=None`` is hermetic. ``Agent.prompt`` creates, sends, waits,
and disposes, so the throwaway turn never pollutes the working agent.
"""

from __future__ import annotations

from collections.abc import Callable

from cursor_sdk import Agent, AgentOptions

from cursorloop.application.dto import TurnOutcome
from cursorloop.domain.model_profile import SHIPPED_PRESETS, ModelProfile
from cursorloop.infrastructure.agent.options import build_agent_options
from cursorloop.infrastructure.agent.translate import outcome_from_run, signals_from_exception

_PROBE_NAME = "cursorloop-probe"
_PROBE_PROMPT = "ok"


def build_probe_options(
    *,
    cwd: str,
    profile: ModelProfile | None = None,
) -> AgentOptions:
    """Pure-ish builder so probe options are testable without a live client.

    ``auto_review`` stays False and ``mode`` stays ``"agent"`` because
    ``build_agent_options`` hard-defaults both. Grok ``effort`` survives on
    ModelSelection params because that builder is the only mapping site.
    """
    return build_agent_options(
        profile=profile if profile is not None else SHIPPED_PRESETS["composer"],
        cwd=cwd,
        tools=[],
        name=_PROBE_NAME,
        setting_sources=None,
    )


def _is_cursor_agent_error(exc: BaseException) -> bool:
    return any(cls.__name__ == "CursorAgentError" for cls in type(exc).__mro__)


def _default_prompt(message: object, options: object, **kwargs: object) -> object:
    return Agent.prompt(message, options, **kwargs)  # type: ignore[arg-type]


class CursorCapacityProbe:
    """Cheap throwaway capacity check via ``Agent.prompt(tools=[])``."""

    def __init__(
        self,
        cwd: str,
        profile: ModelProfile,
        *,
        prompt: Callable[..., object] | None = None,
    ) -> None:
        self._cwd = cwd
        self._profile = profile
        self._prompt = prompt if prompt is not None else _default_prompt

    async def probe(self) -> TurnOutcome:
        options = build_probe_options(cwd=self._cwd, profile=self._profile)
        try:
            result = self._prompt(_PROBE_PROMPT, options)
        except Exception as exc:
            if _is_cursor_agent_error(exc):
                return TurnOutcome(
                    signals=signals_from_exception(exc),
                    verdict=None,
                    output_text="",
                    cost_usd=None,
                    cost_pending=True,
                )
            raise
        text = getattr(result, "result", None)
        buffered = text if isinstance(text, str) else ""
        return outcome_from_run(result, buffered)
