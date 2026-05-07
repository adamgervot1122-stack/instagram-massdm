"""Pipeline orchestrator — runs the agent DAG."""

from __future__ import annotations

import asyncio
from typing import Any

import structlog

from .agents import REGISTRY
from .types import AgentName, AgentRunInput, AgentRunOutput, Verdict

log = structlog.get_logger()


# Layered DAG. Items in the same layer run in parallel.
LAYERS: list[list[AgentName]] = [
    [AgentName.trend_hunter],
    [AgentName.seo_hunter, AgentName.reddit_pain, AgentName.social_viral],
    [AgentName.competitor],
    [AgentName.market_score],          # gate
    [AgentName.offer_generator],
    [AgentName.landing_page, AgentName.ppc, AgentName.content_engine],
]

GATE_THRESHOLD = 60


async def _run_agent(
    agent_name: AgentName, input: AgentRunInput
) -> tuple[AgentName, AgentRunOutput]:
    cls = REGISTRY[agent_name]
    output = await cls().run(input)
    return agent_name, output


async def run_pipeline(
    niche: str,
    geo: list[str],
    period_days: int = 90,
    force: bool = False,
) -> dict[str, Any]:
    """Execute the full pipeline. Returns the final dossier."""
    upstream: dict[str, Any] = {}
    runs: dict[str, AgentRunOutput] = {}
    total_cost = 0.0

    for i, layer in enumerate(LAYERS, start=1):
        log.info("pipeline.layer.start", layer=i, agents=[a.value for a in layer])

        input = AgentRunInput(
            niche=niche,
            geo=geo,
            period_days=period_days,
            upstream={k: v.model_dump() for k, v in runs.items()},
        )

        results = await asyncio.gather(*(_run_agent(a, input) for a in layer))
        for agent_name, output in results:
            runs[agent_name.value] = output
            total_cost += output.cost_usd
            log.info(
                "pipeline.agent.done",
                agent=agent_name.value,
                status=output.status,
                cost=output.cost_usd,
            )

        # Gate: stop expensive generation if score too low
        if AgentName.market_score in layer and not force:
            score = runs[AgentName.market_score.value].data.get("score", 0)
            if score < GATE_THRESHOLD:
                log.warning("pipeline.gated", score=score, threshold=GATE_THRESHOLD)
                return _dossier(niche, geo, runs, total_cost, gated=True)

    return _dossier(niche, geo, runs, total_cost, gated=False)


def _dossier(
    niche: str,
    geo: list[str],
    runs: dict[str, AgentRunOutput],
    total_cost: float,
    gated: bool,
) -> dict[str, Any]:
    score_data = runs.get(AgentName.market_score.value)
    score = score_data.data.get("score") if score_data else None
    verdict = score_data.data.get("verdict") if score_data else Verdict.NO_GO.value
    return {
        "niche": niche,
        "geo": geo,
        "score": score,
        "verdict": verdict,
        "gated": gated,
        "agents": {k: v.model_dump() for k, v in runs.items()},
        "cost_usd": round(total_cost, 4),
    }
