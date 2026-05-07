"""SOCIAL VIRAL AI — TikTok / Reels viral pattern extraction."""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput, Citation
from ..util import estimate_cost, safe_json

SYSTEM = """You are SOCIAL VIRAL, a strategist who reverse-engineers viral
TikToks and Reels.

Extract:
  - hooks: opening 0-3s lines (with avg_views, format, hashtags)
  - structures: beat-by-beat templates (PAS, AIDA, story, listicle, …)
  - cta: call-to-action patterns that convert
  - hashtags: trending niche-relevant hashtags

Return ONLY valid JSON: {"hooks":[...], "structures":[...], "cta":[...],
"hashtags":[...]}.
"""


class SocialViralAgent(BaseAgent):
    name = AgentName.social_viral

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        clips = await self._fetch_social(input)

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n\n"
            f"Top viral clips (TikTok Creative Center + Apify stub):\n"
            f"{json.dumps(clips, indent=2)}\n\n"
            "Extract the JSON per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=3500)
        data = safe_json(text, {"hooks": [], "structures": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            citations=[
                Citation(source="tiktok_creative_center", confidence=0.9),
                Citation(source="instagram_reels", confidence=0.7),
            ],
            cost_usd=estimate_cost(usage, self.model),
        )

    async def _fetch_social(self, input: AgentRunInput) -> list[dict[str, Any]]:
        """TODO(v0.2): wire to Apify TikTok + IG scrapers."""
        return [
            {
                "platform": "tiktok",
                "hook": f"POV: you finally fixed your {input.niche}",
                "views": 1_200_000,
                "likes": 89_000,
            }
        ]
