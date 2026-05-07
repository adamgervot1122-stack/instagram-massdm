"""PPC AI — Meta / TikTok / Google campaign briefs + creatives."""

from __future__ import annotations

import json

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput
from ..util import estimate_cost, safe_json

SYSTEM = """You are PPC, a media buyer who has spent $50M+ at break-even ROAS.

For each platform (meta, tiktok, google) output one or more campaigns:

{
  "campaigns": [
    {
      "platform": "meta|tiktok|google",
      "objective": "sales|leads|traffic",
      "budget_daily": 150,
      "audiences": [{"name":"...", "size_est": "...", "targeting": {...}}],
      "creatives": [
        {"format":"UGC 9:16","hook":"...","script":"...","cta":"..."}
      ],
      "scaling_strategy": "...",
      "kill_criteria": "..."
    }
  ]
}

Be specific: real interests, real CTAs, real budgets per geo. Return ONLY the
JSON.
"""


class PPCAgent(BaseAgent):
    name = AgentName.ppc

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        offer = input.upstream.get("offer_generator", {})
        viral = input.upstream.get("social_viral", {})
        seo = input.upstream.get("seo_hunter", {})

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n\n"
            f"Offer:\n{json.dumps(offer, indent=2)[:3000]}\n\n"
            f"Top hooks:\n{json.dumps(viral, indent=2)[:2000]}\n\n"
            f"Search intent:\n{json.dumps(seo, indent=2)[:2000]}\n\n"
            "Output campaigns per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=4500)
        data = safe_json(text, {"campaigns": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            cost_usd=estimate_cost(usage, self.model),
        )
