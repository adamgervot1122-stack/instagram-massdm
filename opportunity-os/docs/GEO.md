# Geographic analyzer

Each opportunity is scored independently per country. The geo agent enriches
the base scoring with per-country signals.

## Default country set

`US, UK, CA, FR, DE, ES, BR, MX, AR, PL, RO, AU`

(extensible per workspace via `geo.config.yaml`)

## Per-country dimensions

| Dimension | Source |
|---|---|
| CPM (Meta / TikTok / Google) | Meta Ads Library benchmarks, TikTok CC, internal log |
| Competitive density | SimilarWeb top-100, SERP overlap |
| Purchasing power (PPP-adj.) | World Bank PPP, OECD |
| Digital adoption | We Are Social Digital Report |
| TikTok virality coefficient | Creative Center per-region top-50 share rate |
| Logistics difficulty | shipping zones, customs, last-mile cost |
| Estimated CAC | (CPM / CTR) / CVR per category benchmarks |
| Regulatory risk | category-specific (FDA, MHRA, ANSM, ANVISA, etc.) |

## Output

```json
{
  "geo_ranking": [
    {"country":"US","score":86,"tier":"TOP","cac_est":18.4,"cpm":12.3},
    {"country":"DE","score":71,"tier":"BLUE_OCEAN","cac_est":9.1,"cpm":7.2},
    {"country":"BR","score":48,"tier":"WATCH","cac_est":4.2,"cpm":3.1},
    {"country":"FR","score":34,"tier":"AVOID","reason":"regulated category"}
  ],
  "recommended_launch_sequence": ["US","DE","UK"]
}
```

## Recommendation logic

1. Sort by per-geo `score` desc
2. Filter out `regulatory_risk >= 8`
3. Bucket:
   - **TOP**: score ≥ 75
   - **BLUE OCEAN**: demand high + competition low (rule-based override)
   - **WATCH**: 50 ≤ score < 75
   - **AVOID**: score < 50 or hard-blocked
4. Suggest a 90-day rollout: `[primary, secondary, tertiary]` mixing one
   TOP and one BLUE OCEAN to balance scale and margin.
