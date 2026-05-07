# Scoring engine

`market_score` produces a single 0–100 score and a GO / NO-GO verdict.
The score is a **weighted, normalised** combination of 10 sub-scores.

## Sub-scores (each 0–10)

| # | Sub-score | Weight | Driver |
|---|---|---:|---|
| 1 | demand | 1.4 | trend velocity, search volume, Reddit pain frequency |
| 2 | competition | 1.2 | inverted: SERP DR avg, top-3 ad density, market saturation |
| 3 | branding_potential | 1.0 | name availability, emotional pull, USP novelty |
| 4 | retention | 1.1 | category baseline LTV/CAC, churn benchmarks |
| 5 | ltv | 1.1 | predicted AOV × purchase frequency × lifespan |
| 6 | virality | 1.2 | TikTok hook performance, sharing coefficient |
| 7 | seo | 0.9 | long-tail breadth × KD-weighted CPC |
| 8 | ppc | 0.9 | CPM × CTR benchmarks per geo |
| 9 | scalability_3y | 1.1 | TAM × geographic expansion × supply elasticity |
| 10 | technical_difficulty | 1.1 | inverted: ops + supply + regulatory complexity |

```
score = clip( Σ (sub_i * weight_i) / Σ weight_i * 10 , 0, 100 )
```

## Verdict thresholds

| Score | Verdict |
|---|---|
| ≥ 75 | GO |
| 60–74 | GO_WITH_RESERVES |
| 45–59 | NO_GO_NOW (revisit in 90d) |
| < 45 | NO_GO |

## Per-geo scoring

The same model runs per ISO country. Final pipeline output ranks geos:

- **TOP MARKETS** — score ≥ 75
- **BLUE OCEAN** — demand ≥ 8 AND competition ≤ 4
- **AVOID** — score < 45 OR regulatory_risk ≥ 8

## Tunability

Weights live in `apps/agents/agents/market_score/config.yaml` so a workspace
can up-weight retention vs virality (e.g. SaaS vs DTC physical product).
