"""Smoke tests — no LLM calls."""

from opportunity_os.agents import REGISTRY
from opportunity_os.geo import score_geos
from opportunity_os.pipeline import LAYERS
from opportunity_os.types import AgentName


def test_all_agents_registered() -> None:
    assert set(REGISTRY.keys()) == set(AgentName)


def test_all_agents_appear_in_dag() -> None:
    in_dag = {a for layer in LAYERS for a in layer}
    assert in_dag == set(AgentName)


def test_geo_scoring_returns_sorted_results() -> None:
    subs = {
        "demand": 8, "competition": 6, "branding_potential": 7, "retention": 7,
        "ltv": 7, "virality": 8, "seo": 7, "ppc": 7, "scalability_3y": 8,
        "technical_difficulty": 6,
    }
    out = score_geos("sleep aid", ["US", "FR", "BR"], subs)
    assert len(out) == 3
    scores = [g.score for g in out]
    assert scores == sorted(scores, reverse=True)


def test_geo_unknown_country_uses_defaults() -> None:
    subs = {k: 5 for k in (
        "demand", "competition", "branding_potential", "retention", "ltv",
        "virality", "seo", "ppc", "scalability_3y", "technical_difficulty",
    )}
    out = score_geos("x", ["ZZ"], subs)
    assert out[0].country == "ZZ"
    assert 0 <= out[0].score <= 100
