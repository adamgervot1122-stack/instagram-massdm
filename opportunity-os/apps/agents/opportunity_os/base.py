"""Base class shared by every agent."""

from __future__ import annotations

import hashlib
import json
import time
from abc import ABC, abstractmethod
from typing import Any

import structlog
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import settings
from .types import AgentName, AgentRunInput, AgentRunOutput

log = structlog.get_logger()


class BaseAgent(ABC):
    """Lifecycle:
        run(input) ──► _execute(input) ──► AgentRunOutput
    Subclasses implement `_execute`.
    """

    name: AgentName
    model: str = settings.primary_model

    def __init__(self) -> None:
        self.anthropic = AsyncAnthropic(api_key=settings.anthropic_api_key)

    # ───────────────────────── public API ─────────────────────────

    async def run(self, input: AgentRunInput) -> AgentRunOutput:
        started = time.perf_counter()
        log.info("agent.start", agent=self.name.value, niche=input.niche)
        try:
            output = await self._execute(input)
        except Exception as exc:  # noqa: BLE001
            log.exception("agent.failed", agent=self.name.value)
            return AgentRunOutput(
                agent=self.name,
                status="failed",
                error=str(exc),
                latency_ms=int((time.perf_counter() - started) * 1000),
                model=self.model,
            )
        output.latency_ms = int((time.perf_counter() - started) * 1000)
        output.model = output.model or self.model
        log.info(
            "agent.ok",
            agent=self.name.value,
            ms=output.latency_ms,
            cost=output.cost_usd,
        )
        return output

    # ───────────────────────── helpers ─────────────────────────

    def prompt_hash(self, input: AgentRunInput) -> str:
        """Stable cache key for `(agent, niche, geo, period)`."""
        payload = json.dumps(
            {
                "agent": self.name.value,
                "niche": input.niche,
                "geo": sorted(input.geo),
                "period_days": input.period_days,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def _llm(
        self,
        system: str,
        user: str,
        max_tokens: int = 4000,
        cache_system: bool = True,
    ) -> tuple[str, dict[str, Any]]:
        """Thin wrapper around Claude, with prompt-caching on the system prompt."""
        msg = await self.anthropic.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=(
                [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
                if cache_system
                else system
            ),
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(block.text for block in msg.content if block.type == "text")
        usage = {
            "input_tokens": msg.usage.input_tokens,
            "output_tokens": msg.usage.output_tokens,
            "cache_read_tokens": getattr(msg.usage, "cache_read_input_tokens", 0),
            "cache_create_tokens": getattr(msg.usage, "cache_creation_input_tokens", 0),
        }
        return text, usage

    @abstractmethod
    async def _execute(self, input: AgentRunInput) -> AgentRunOutput: ...
