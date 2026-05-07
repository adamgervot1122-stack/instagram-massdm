"""REDDIT PAIN AI — extracts user frustrations + emotional language."""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..types import AgentName, AgentRunInput, AgentRunOutput, Citation
from ..util import estimate_cost, safe_json

SYSTEM = """You are REDDIT PAIN, an ethnographer who reads thousands of Reddit
threads to surface the *exact* language users use about their pain.

For each pain theme, return:
  - theme (short noun phrase)
  - frequency (0..1, share of threads mentioning it)
  - intensity (0..1, severity of language)
  - verbatim (3-5 *exact* quotes — do NOT paraphrase)
  - subs (subreddits where it shows up)

Also extract emotional_register (3-5 dominant emotions: frustrated,
desperate, skeptical, hopeful, betrayed, etc.).

Return ONLY valid JSON: {"pains":[...], "emotional_register":[...]}.
Verbatim quotes must come from the input — never invent them.
"""


class RedditPainAgent(BaseAgent):
    name = AgentName.reddit_pain

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        threads = await self._fetch_reddit(input)

        user = (
            f"Niche: {input.niche}\n\n"
            f"Top threads + comments (PRAW stub):\n{json.dumps(threads, indent=2)}\n\n"
            "Surface pain themes per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=3000)
        data = safe_json(text, {"pains": [], "emotional_register": []})

        return AgentRunOutput(
            agent=self.name,
            data=data,
            citations=[Citation(source="reddit", confidence=0.8)],
            cost_usd=estimate_cost(usage, self.model),
        )

    async def _fetch_reddit(self, input: AgentRunInput) -> list[dict[str, Any]]:
        """TODO(v0.2): wire to PRAW + niche-relevant subs."""
        return [
            {
                "sub": f"r/{input.niche.replace(' ', '')}",
                "title": f"Anyone else struggling with {input.niche}?",
                "score": 412,
                "comments": 89,
            }
        ]
