"""CONTENT ENGINE AI — TikTok scripts, UGC briefs, tweets, blog posts."""

from __future__ import annotations

import json

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput
from ..util import estimate_cost, safe_json

SYSTEM = """You are CONTENT ENGINE, a senior creative strategist.

Output a content kit:

{
  "tiktok_scripts": [   // 5 scripts
    {"hook":"...","beats":["...","..."],"cta":"...","style":"..."}
  ],
  "ugc_briefs": [       // 3 briefs
    {"creator_archetype":"...","brief":"...","talking_points":[...]}
  ],
  "tweets": [            // 10 tweets
    {"text":"...","cta":"..."}
  ],
  "blog_posts": [        // 3 SEO posts
    {"title":"...","h1":"...","outline":["..."],"target_kw":"..."}
  ]
}

Use the niche's verbatim language from upstream pains. Return ONLY the JSON.
"""


class ContentEngineAgent(BaseAgent):
    name = AgentName.content_engine

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        offer = input.upstream.get("offer_generator", {})
        pains = input.upstream.get("reddit_pain", {})
        viral = input.upstream.get("social_viral", {})
        seo = input.upstream.get("seo_hunter", {})

        user = (
            f"Niche: {input.niche}\n\n"
            f"Offer:\n{json.dumps(offer, indent=2)[:2500]}\n\n"
            f"Pains:\n{json.dumps(pains, indent=2)[:2500]}\n\n"
            f"Viral patterns:\n{json.dumps(viral, indent=2)[:2000]}\n\n"
            f"SEO targets:\n{json.dumps(seo, indent=2)[:2000]}\n\n"
            "Output the content kit per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=5500)
        data = safe_json(text, {"tiktok_scripts": [], "ugc_briefs": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            cost_usd=estimate_cost(usage, self.model),
        )
