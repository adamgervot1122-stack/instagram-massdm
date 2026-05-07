"""COMPETITOR AI — traffic, pricing, USP gaps."""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput, Citation
from ..util import estimate_cost, safe_json

SYSTEM = """You are COMPETITOR, head of competitive intelligence.

For each top competitor, return:
  - domain, traffic (monthly visits), top_kw (3-5)
  - pricing ({tier: monthly_price})
  - weaknesses (3-5 concrete weaknesses — be specific)

Then output 3-5 "gaps": un-served sub-segments or angles. Each gap must be
defensible — back it up with implicit reasoning from the data.

Return ONLY valid JSON: {"competitors":[...], "gaps":[...],
"saturation": 0..1, "differentiation_angles":[...]}.
"""


class CompetitorAgent(BaseAgent):
    name = AgentName.competitor

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        comps = await self._fetch_competitors(input)
        upstream = {
            "trends": input.upstream.get("trend_hunter", {}),
            "seo": input.upstream.get("seo_hunter", {}),
        }

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n\n"
            f"Top competitors (SimilarWeb + SEMrush + Meta Ads Lib stub):\n"
            f"{json.dumps(comps, indent=2)}\n\n"
            f"Upstream context:\n{json.dumps(upstream, indent=2)}\n\n"
            "Synthesise per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=3500)
        data = safe_json(text, {"competitors": [], "gaps": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            citations=[
                Citation(source="similarweb", confidence=0.8),
                Citation(source="meta_ads_library", confidence=0.85),
            ],
            cost_usd=estimate_cost(usage, self.model),
        )

    async def _fetch_competitors(self, input: AgentRunInput) -> list[dict[str, Any]]:
        """TODO(v0.2): wire to SimilarWeb + SEMrush + Meta Ads Library APIs."""
        return [
            {"domain": f"{input.niche.split()[0]}market.com", "traffic": 4_200_000},
            {"domain": f"buy{input.niche.split()[0]}.io", "traffic": 1_100_000},
        ]
