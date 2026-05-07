"""FastAPI sidecar — exposes /run/{agent} and /pipeline."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agents import REGISTRY
from .pipeline import run_pipeline
from .types import AgentName, AgentRunInput

app = FastAPI(title="OPPORTUNITY OS — agents API", version="0.1.0")


class PipelineRequest(BaseModel):
    niche: str
    geo: list[str]
    period_days: int = 90
    force: bool = False


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/pipeline")
async def pipeline(req: PipelineRequest) -> dict[str, Any]:
    return await run_pipeline(
        niche=req.niche,
        geo=req.geo,
        period_days=req.period_days,
        force=req.force,
    )


@app.post("/run/{agent_name}")
async def run_agent(agent_name: str, input: AgentRunInput) -> dict[str, Any]:
    try:
        name = AgentName(agent_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_name}") from exc
    output = await REGISTRY[name]().run(input)
    return output.model_dump()
