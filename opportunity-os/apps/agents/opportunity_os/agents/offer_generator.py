"""OFFER GENERATOR AI — synthesises the offer + USP + pricing + brand angle."""

from __future__ import annotations

import json

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput
from ..util import estimate_cost, safe_json

SYSTEM = """You are OFFER GENERATOR, a YC-grade founder + brand strategist.

Given trend / SEO / pain / viral / competitor signals, synthesise ONE
high-conviction offer:

{
  "offer": {
    "name": "...",            // brandable, 1-2 words ideally
    "format": "...",          // physical product, SaaS, service, course, …
    "price": {"month": ..., "trial": ..., "year": ...},
    "usp": "...",             // one line, defensible
    "positioning": "...",     // who it's for vs alternatives
    "emotional_angle": "...", // what they'll feel
    "hero_promise": "..."     // the one-line promise on the hero section
  },
  "icp": {
    "demographic": "...",
    "psychographic": "...",
    "jtbd": "...",            // job to be done
    "willingness_to_pay": "..."
  },
  "branding": {
    "name": "...", "slogan": "...", "tone_of_voice": [...],
    "palette": ["#...","#...","#..."], "font": "..."
  }
}

Be specific, not generic. No fluff. Return ONLY the JSON.
"""


class OfferGeneratorAgent(BaseAgent):
    name = AgentName.offer_generator

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        ctx = {
            "trends": input.upstream.get("trend_hunter", {}),
            "seo": input.upstream.get("seo_hunter", {}),
            "pains": input.upstream.get("reddit_pain", {}),
            "viral": input.upstream.get("social_viral", {}),
            "competitors": input.upstream.get("competitor", {}),
        }

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n\n"
            f"Upstream synthesis:\n{json.dumps(ctx, indent=2)[:8000]}\n\n"
            "Synthesise the offer per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=3000)
        data = safe_json(text, {})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            cost_usd=estimate_cost(usage, self.model),
        )
