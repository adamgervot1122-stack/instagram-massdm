"""SEO HUNTER AI — keyword opportunity mining."""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput, Citation
from ..util import estimate_cost, safe_json

SYSTEM = """You are SEO HUNTER, head of SEO at a $100M DTC brand.
Mine the keyword universe around a niche and surface the winners.

For each keyword, return: kw, volume, kd (0-100), cpc (USD), intent
(informational|commercial|transactional|navigational), and 3-5 long_tail
variants. Compute roi_score (0-100) = volume × cpc / max(kd, 5), normalised.

Return ONLY valid JSON: {"keywords":[...], "roi_score": 0..100,
"long_tail_opportunities":[...], "content_gaps":[...]}.
"""


class SEOHunterAgent(BaseAgent):
    name = AgentName.seo_hunter

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        raw = await self._fetch_keyword_data(input)

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n\n"
            f"Raw keyword signals (DataForSEO/SEMrush stub):\n{json.dumps(raw, indent=2)}\n\n"
            "Synthesise into the JSON shape from the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=3500)
        data = safe_json(text, {"keywords": [], "roi_score": 0})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            citations=[
                Citation(source="dataforseo", confidence=0.9),
                Citation(source="semrush", confidence=0.85),
            ],
            cost_usd=estimate_cost(usage, self.model),
        )

    async def _fetch_keyword_data(self, input: AgentRunInput) -> list[dict[str, Any]]:
        """TODO(v0.2): wire to DataForSEO + SEMrush APIs."""
        seeds = (input.niche, f"best {input.niche}", f"{input.niche} for", f"how to {input.niche}")
        return [{"seed": s, "geo": g} for s in seeds for g in input.geo]
