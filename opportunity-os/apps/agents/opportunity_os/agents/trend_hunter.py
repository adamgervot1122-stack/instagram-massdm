"""TREND HUNTER AI — detects emerging Google Trends + micro-trends."""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput, Citation
from ..util import estimate_cost, safe_json

SYSTEM = """You are TREND HUNTER, an elite trend analyst at a $100M DTC fund.
You synthesise Google Trends + Exploding Topics + cultural micro-trends into
actionable opportunity signals.

For each emerging keyword, return:
  - velocity_30d (multiplier vs 90d baseline; >1.0 = growing)
  - saturation (0..1, share of SERP top-10 owned by big brands)
  - viral_score (0..100)
  - regions (ISO-3166 alpha-2)

Return ONLY valid JSON matching this exact shape:
{"trends":[{...}], "micro_trends":[{...}]}

Be ruthless: prefer 5 high-confidence trends over 20 noisy ones.
"""


class TrendHunterAgent(BaseAgent):
    name = AgentName.trend_hunter

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        raw_trends = await self._fetch_trends(input)

        user = (
            f"Niche: {input.niche}\n"
            f"Target geos: {','.join(input.geo)}\n"
            f"Period: last {input.period_days} days\n\n"
            f"Raw Google Trends signals:\n{json.dumps(raw_trends, indent=2)}\n\n"
            "Synthesise into the JSON shape described in the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=2500)
        data = safe_json(text, {"trends": [], "micro_trends": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            citations=[
                Citation(source="google_trends", confidence=0.85),
                Citation(source="exploding_topics", confidence=0.75),
            ],
            cost_usd=estimate_cost(usage, self.model),
        )

    async def _fetch_trends(self, input: AgentRunInput) -> list[dict[str, Any]]:
        """Pull raw signals.

        TODO(v0.2): wire to pytrends. For now we return a stub the LLM can
        reason over so the pipeline runs end-to-end.
        """
        return [
            {
                "keyword": f"{input.niche} {modifier}",
                "geo": geo,
                "value_now": 78,
                "value_baseline": 42,
            }
            for modifier in ("near me", "review", "vs", "alternative", "best 2026")
            for geo in input.geo
        ]


