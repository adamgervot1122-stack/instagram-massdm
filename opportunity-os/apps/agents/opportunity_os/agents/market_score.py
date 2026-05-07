"""MARKET SCORE AI — /100 score + GO/NO-GO verdict.

This agent is intentionally **deterministic**: it computes sub-scores from
the upstream agents' structured outputs using a fixed weighting (see
`docs/SCORING.md`), then asks the LLM only for risks + next_actions.

Why? Because a stable score is auditable. A pure-LLM score isn't.
"""

from __future__ import annotations

import json
from typing import Any

from ..base import BaseAgent
from ..geo import score_geos
from ..types import AgentName, AgentRunInput, AgentRunOutput, Verdict
from ..util import estimate_cost, safe_json

# (sub_name, weight)
WEIGHTS: dict[str, float] = {
    "demand": 1.4,
    "competition": 1.2,
    "branding_potential": 1.0,
    "retention": 1.1,
    "ltv": 1.1,
    "virality": 1.2,
    "seo": 0.9,
    "ppc": 0.9,
    "scalability_3y": 1.1,
    "technical_difficulty": 1.1,  # inverted upstream
}

SYSTEM = """You are MARKET SCORE risk analyst.

Given the niche + sub-scores, output:
{
  "risks": ["..."],          // 3-6 concrete risks (regulatory, supply, CAC, channel)
  "next_actions": ["..."]    // 5-8 specific actions for the next 30 days
}

Return ONLY the JSON. Be specific — no platitudes.
"""


def _clip(x: float, lo: float = 0, hi: float = 10) -> float:
    return max(lo, min(hi, x))


def _compute_subscores(upstream: dict[str, Any]) -> dict[str, int]:
    trend = upstream.get("trend_hunter", {}).get("data", upstream.get("trend_hunter", {}))
    seo = upstream.get("seo_hunter", {}).get("data", upstream.get("seo_hunter", {}))
    pain = upstream.get("reddit_pain", {}).get("data", upstream.get("reddit_pain", {}))
    viral = upstream.get("social_viral", {}).get("data", upstream.get("social_viral", {}))
    comp = upstream.get("competitor", {}).get("data", upstream.get("competitor", {}))

    # demand: normalised trend velocity × pain frequency
    velocities = [t.get("velocity_30d", 1.0) for t in trend.get("trends", [])]
    pain_freqs = [p.get("frequency", 0) for p in pain.get("pains", [])]
    avg_v = sum(velocities) / max(len(velocities), 1)
    avg_p = sum(pain_freqs) / max(len(pain_freqs), 1)
    demand = _clip((avg_v - 0.8) * 6 + avg_p * 6)

    # competition: inverted saturation + gap count
    saturation = comp.get("saturation", 0.6)
    gaps = len(comp.get("gaps", []))
    competition = _clip((1 - saturation) * 8 + min(gaps, 5) * 0.4)

    # virality: avg viral_score / 10
    viral_scores = [t.get("viral_score", 0) for t in trend.get("trends", [])]
    hooks = viral.get("hooks", [])
    hook_perf = sum(min(h.get("avg_views", 0) / 200_000, 10) for h in hooks) / max(len(hooks), 1)
    virality = _clip((sum(viral_scores) / max(len(viral_scores), 1)) / 10 * 0.6 + hook_perf * 0.4)

    # seo: roi_score / 10 + long-tail breadth
    roi = seo.get("roi_score", 0)
    long_tail = sum(len(k.get("long_tail", [])) for k in seo.get("keywords", []))
    seo_score = _clip(roi / 10 * 0.7 + min(long_tail, 30) / 30 * 3)

    # ppc: derived from CPCs (lower CPC, higher ppc score)
    cpcs = [k.get("cpc", 0) for k in seo.get("keywords", []) if k.get("cpc", 0) > 0]
    avg_cpc = sum(cpcs) / max(len(cpcs), 1) if cpcs else 1.5
    ppc_score = _clip(8 - avg_cpc * 1.2)

    # heuristic priors (caller can override per-category)
    branding = 7
    retention = 7
    ltv = 7
    scalability = 7
    tech = 6  # inverted: low difficulty = high score

    return {
        "demand": round(demand),
        "competition": round(competition),
        "branding_potential": branding,
        "retention": retention,
        "ltv": ltv,
        "virality": round(virality),
        "seo": round(seo_score),
        "ppc": round(ppc_score),
        "scalability_3y": scalability,
        "technical_difficulty": tech,
    }


def _aggregate(subs: dict[str, int]) -> int:
    total_w = sum(WEIGHTS.values())
    weighted = sum(subs[k] * WEIGHTS[k] for k in WEIGHTS)
    return round(max(0, min(100, (weighted / total_w) * 10)))


def _verdict(score: int) -> Verdict:
    if score >= 75:
        return Verdict.GO
    if score >= 60:
        return Verdict.GO_WITH_RESERVES
    if score >= 45:
        return Verdict.NO_GO_NOW
    return Verdict.NO_GO


class MarketScoreAgent(BaseAgent):
    name = AgentName.market_score

    async def _execute(self, input: AgentRunInput) -> AgentRunOutput:
        subs = _compute_subscores(input.upstream)
        score = _aggregate(subs)
        verdict = _verdict(score)
        geo_ranking = score_geos(input.niche, input.geo, subs)

        user = (
            f"Niche: {input.niche}\nGeos: {','.join(input.geo)}\n"
            f"Sub-scores: {json.dumps(subs)}\n"
            f"Total score: {score} → verdict: {verdict.value}\n\n"
            "Surface risks + next_actions per the system prompt."
        )
        text, usage = await self._llm(SYSTEM, user, max_tokens=1500)
        risk_data = safe_json(text, {"risks": [], "next_actions": []})

        return AgentRunOutput(
            agent=self.name,
            data={
                "score": score,
                "verdict": verdict.value,
                "subscores": subs,
                "geo_ranking": [g.model_dump() for g in geo_ranking],
                "risks": risk_data.get("risks", []),
                "next_actions": risk_data.get("next_actions", []),
            },
            cost_usd=estimate_cost(usage, self.model),
        )
