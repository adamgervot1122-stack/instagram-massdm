"""Shared pydantic types for the agent layer."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    trend_hunter = "trend_hunter"
    seo_hunter = "seo_hunter"
    reddit_pain = "reddit_pain"
    social_viral = "social_viral"
    competitor = "competitor"
    offer_generator = "offer_generator"
    landing_page = "landing_page"
    ppc = "ppc"
    content_engine = "content_engine"
    market_score = "market_score"


class Verdict(str, Enum):
    GO = "GO"
    GO_WITH_RESERVES = "GO_WITH_RESERVES"
    NO_GO_NOW = "NO_GO_NOW"
    NO_GO = "NO_GO"


class GeoTier(str, Enum):
    TOP = "TOP"
    BLUE_OCEAN = "BLUE_OCEAN"
    WATCH = "WATCH"
    AVOID = "AVOID"


class Citation(BaseModel):
    source: str
    url: str | None = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    confidence: float = Field(ge=0, le=1, default=0.7)


class AgentRunInput(BaseModel):
    niche: str
    geo: list[str]
    period_days: int = 90
    workspace_id: UUID = Field(default_factory=uuid4)
    cache: bool = True
    upstream: dict[str, Any] = Field(default_factory=dict)
    """Outputs from upstream agents (key = AgentName.value)."""


class AgentRunOutput(BaseModel):
    agent: AgentName
    status: Literal["ok", "partial", "failed"] = "ok"
    data: dict[str, Any] = Field(default_factory=dict)
    citations: list[Citation] = Field(default_factory=list)
    cost_usd: float = 0.0
    latency_ms: int = 0
    model: str | None = None
    error: str | None = None


# ───────────────────────── domain payloads ─────────────────────────


class TrendPoint(BaseModel):
    keyword: str
    velocity_30d: float
    saturation: float = Field(ge=0, le=1)
    viral_score: int = Field(ge=0, le=100)
    regions: list[str] = Field(default_factory=list)


class KeywordRow(BaseModel):
    kw: str
    volume: int
    kd: int
    cpc: float
    intent: Literal["informational", "commercial", "transactional", "navigational"]
    long_tail: list[str] = Field(default_factory=list)


class PainPoint(BaseModel):
    theme: str
    frequency: float
    intensity: float
    verbatim: list[str] = Field(default_factory=list)
    subs: list[str] = Field(default_factory=list)


class ViralHook(BaseModel):
    text: str
    format: str
    avg_views: int
    hashtags: list[str] = Field(default_factory=list)


class CompetitorRow(BaseModel):
    domain: str
    traffic: int | None = None
    top_kw: list[str] = Field(default_factory=list)
    pricing: dict[str, float] = Field(default_factory=dict)
    weaknesses: list[str] = Field(default_factory=list)


class Offer(BaseModel):
    name: str
    format: str
    price: dict[str, float]
    usp: str
    positioning: str
    emotional_angle: str


class GeoScore(BaseModel):
    country: str
    score: int
    tier: GeoTier
    cac_est: float | None = None
    cpm: float | None = None
    reason: str | None = None


class MarketScore(BaseModel):
    score: int = Field(ge=0, le=100)
    verdict: Verdict
    subscores: dict[str, int]
    risks: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    geo_ranking: list[GeoScore] = Field(default_factory=list)
