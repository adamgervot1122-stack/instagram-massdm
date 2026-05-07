"""Geographic analyzer — scores opportunity per ISO country.

Per-geo signals are static benchmarks for v0.1; in v0.2 they'll be
hydrated from Meta Ads Library + We Are Social Digital Reports.
"""

from __future__ import annotations

from .types import GeoScore, GeoTier

# Per-country priors. Numbers are illustrative benchmarks meant to be
# overridden in `geo.config.yaml` per workspace.
GEO_PRIORS: dict[str, dict[str, float]] = {
    "US": {"cpm": 12.3, "ppp": 1.00, "digital": 0.95, "viral": 0.90, "logistics": 0.95},
    "UK": {"cpm": 9.1, "ppp": 0.95, "digital": 0.92, "viral": 0.85, "logistics": 0.90},
    "CA": {"cpm": 8.4, "ppp": 0.90, "digital": 0.92, "viral": 0.82, "logistics": 0.88},
    "FR": {"cpm": 6.8, "ppp": 0.85, "digital": 0.85, "viral": 0.80, "logistics": 0.85},
    "DE": {"cpm": 7.2, "ppp": 0.92, "digital": 0.88, "viral": 0.70, "logistics": 0.92},
    "ES": {"cpm": 4.5, "ppp": 0.78, "digital": 0.80, "viral": 0.78, "logistics": 0.80},
    "BR": {"cpm": 3.1, "ppp": 0.45, "digital": 0.78, "viral": 0.92, "logistics": 0.55},
    "MX": {"cpm": 2.9, "ppp": 0.50, "digital": 0.72, "viral": 0.85, "logistics": 0.60},
    "AR": {"cpm": 2.3, "ppp": 0.30, "digital": 0.70, "viral": 0.80, "logistics": 0.50},
    "PL": {"cpm": 3.4, "ppp": 0.65, "digital": 0.82, "viral": 0.72, "logistics": 0.78},
    "RO": {"cpm": 2.8, "ppp": 0.55, "digital": 0.78, "viral": 0.70, "logistics": 0.72},
    "AU": {"cpm": 10.1, "ppp": 0.95, "digital": 0.92, "viral": 0.85, "logistics": 0.85},
}

DEFAULT_PRIOR = {"cpm": 6.0, "ppp": 0.7, "digital": 0.75, "viral": 0.7, "logistics": 0.75}


def _per_country_score(country: str, base_subs: dict[str, int]) -> tuple[int, dict[str, float]]:
    p = GEO_PRIORS.get(country, DEFAULT_PRIOR)
    base = sum(base_subs.values()) / len(base_subs)  # 0..10

    # blend base with geo modifiers
    digital = p["digital"] * 10
    viral = p["viral"] * 10
    ppp = p["ppp"] * 10
    log = p["logistics"] * 10
    cpm_score = max(0, 10 - p["cpm"] / 2)  # lower cpm = better

    geo_score = (digital * 0.2 + viral * 0.25 + ppp * 0.2 + log * 0.15 + cpm_score * 0.2)
    blended = round((base * 0.5 + geo_score * 0.5) * 10)
    blended = max(0, min(100, blended))

    # crude CAC estimate: CPM / assumed CTR / assumed CVR
    cac_est = round(p["cpm"] / 0.012 / 0.025, 2)
    return blended, {"cac_est": cac_est, "cpm": p["cpm"]}


def _tier(score: int, base_subs: dict[str, int]) -> GeoTier:
    demand = base_subs.get("demand", 5)
    competition = base_subs.get("competition", 5)
    if demand >= 8 and competition >= 7:
        return GeoTier.BLUE_OCEAN
    if score >= 75:
        return GeoTier.TOP
    if score >= 50:
        return GeoTier.WATCH
    return GeoTier.AVOID


def score_geos(niche: str, geos: list[str], base_subs: dict[str, int]) -> list[GeoScore]:
    out: list[GeoScore] = []
    for c in geos:
        score, extra = _per_country_score(c, base_subs)
        out.append(
            GeoScore(
                country=c,
                score=score,
                tier=_tier(score, base_subs),
                cac_est=extra["cac_est"],
                cpm=extra["cpm"],
            )
        )
    out.sort(key=lambda g: g.score, reverse=True)
    return out
