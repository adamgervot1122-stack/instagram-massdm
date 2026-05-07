"""LANDING PAGE AI — generates a full conversion-optimised landing page."""

from __future__ import annotations

import json

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput
from ..util import estimate_cost, safe_json

SYSTEM = """You are LANDING PAGE, a conversion-rate-optimisation specialist.

Given the offer + ICP + brand, output a complete landing page:

{
  "sections": [
    {"type": "hero", "h1": "...", "sub": "...", "cta": "...", "social_proof": "..."},
    {"type": "problem", "title": "...", "bullets": [...]},
    {"type": "solution", "title": "...", "bullets": [...]},
    {"type": "how_it_works", "steps": [{"title":"...","body":"..."},...]},
    {"type": "benefits", "items": [...]},
    {"type": "social_proof", "testimonials": [...], "logos": [...]},
    {"type": "pricing", "plans": [...]},
    {"type": "faq", "items": [{"q":"...","a":"..."}]},
    {"type": "final_cta", "h2":"...", "cta":"..."}
  ],
  "design_system": {"primary":"#...","accent":"#...","bg":"#...","font":"..."},
  "jsx": "<full Next.js page component string, mobile-first Tailwind>"
}

The JSX must be a single self-contained React component. Use Tailwind v3
classes. Mobile-first. No external images — use gradient placeholders.

Return ONLY the JSON.
"""


class LandingPageAgent(BaseAgent):
    name = AgentName.landing_page

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        offer = input.upstream.get("offer_generator", {})
        pains = input.upstream.get("reddit_pain", {})

        user = (
            f"Niche: {input.niche}\n\n"
            f"Offer + branding:\n{json.dumps(offer, indent=2)[:4000]}\n\n"
            f"Pain points (use verbatim language):\n{json.dumps(pains, indent=2)[:3000]}\n\n"
            "Generate the landing page per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=8000)
        data = safe_json(text, {"sections": [], "jsx": ""})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            cost_usd=estimate_cost(usage, self.model),
        )
