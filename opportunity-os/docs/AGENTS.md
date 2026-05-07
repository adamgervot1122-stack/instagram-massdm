# Agents — I/O contracts

All agents share a common envelope:

```python
class AgentRunInput(BaseModel):
    niche: str
    geo: list[str]            # ISO-3166 alpha-2
    period_days: int = 90
    workspace_id: UUID
    cache: bool = True

class AgentRunOutput(BaseModel):
    agent: str
    status: Literal["ok", "partial", "failed"]
    data: dict                # agent-specific payload
    citations: list[Citation]
    cost_usd: float
    latency_ms: int
    model: str
```

`Citation` includes `{source, url, fetched_at, confidence}` so every claim is
traceable to a real data point.

---

## 1. trend_hunter

**Sources**: pytrends, Glimpse, Exploding Topics RSS

**Output `data`**:
```json
{
  "trends": [
    {"keyword": "magnesium glycinate sleep", "velocity_30d": 1.42,
     "saturation": 0.31, "viral_score": 78, "regions": ["US","CA","UK"]}
  ],
  "micro_trends": [...]
}
```

## 2. seo_hunter

**Sources**: SEMrush API, DataForSEO, Ahrefs MCP, Google Suggest

**Output `data`**:
```json
{
  "keywords": [
    {"kw": "natural sleep aid no melatonin", "volume": 12100,
     "kd": 18, "cpc": 1.84, "intent": "commercial",
     "long_tail": ["best natural sleep aid no melatonin reddit", ...]}
  ],
  "roi_score": 82
}
```

## 3. reddit_pain

**Sources**: Reddit PRAW (top + rising in target subs), Quora, niche forums

**Output `data`**:
```json
{
  "pains": [
    {"theme": "wake up at 3am", "frequency": 0.34, "intensity": 0.81,
     "verbatim": ["I literally wake up at 3am every. single. night."],
     "subs": ["r/insomnia","r/Biohackers"]}
  ],
  "emotional_register": ["frustrated","desperate","skeptical"]
}
```

## 4. social_viral

**Sources**: TikTok Creative Center, Apify TikTok scraper, Instagram Reels via
Apify, YouTube Shorts

**Output `data`**:
```json
{
  "hooks": [
    {"text": "POV: it's 3am and you're staring at the ceiling…",
     "format": "talking-head + b-roll", "avg_views": 1.2e6,
     "hashtags": ["#cantsleep","#sleeptok"]}
  ],
  "structures": [{"name":"PAS","beats":["pain","amplify","solution"]}]
}
```

## 5. competitor

**Sources**: SimilarWeb, Meta Ads Library, store scrapers, SEMrush Domain
Overview

**Output `data`**:
```json
{
  "competitors": [
    {"domain":"calm.com","traffic":18.4e6,"top_kw":["sleep meditation"],
     "pricing":{"month":14.99,"year":69.99},
     "weaknesses":["no science-backed angle","poor mobile checkout"]}
  ],
  "gaps": ["no premium DTC product targeting non-melatonin users 30-45 USA"]
}
```

## 6. offer_generator

**Input**: outputs of agents 1–5

**Output `data`**:
```json
{
  "offer": {
    "name":"NIGHTSHIFT — sleep without melatonin",
    "format":"60-capsule bottle, 30-day supply",
    "price":{"month":39,"trial":19},
    "usp":"the only non-melatonin formula tested for 3am wake-ups",
    "positioning":"premium DTC, science-led, anti-grogginess",
    "emotional_angle":"finally sleep through the night without feeling drugged"
  }
}
```

## 7. landing_page

**Output `data`**:
```json
{
  "html": "<...>",
  "jsx": "<...>",
  "sections": ["hero","problem","solution","social_proof","ingredients",
               "how_it_works","reviews","pricing","faq","footer"],
  "design_system": {"primary":"#0B0B12","accent":"#A6F0C6","font":"Inter"}
}
```

## 8. ppc

**Output `data`** per platform (Meta, TikTok, Google):
```json
{
  "campaigns": [
    {"platform":"meta","objective":"sales",
     "audiences":[{"name":"3am-wakers 30-45 US","interests":["insomnia"]}],
     "creatives":[{"hook":"…","script":"…","format":"UGC 9:16"}],
     "budget_daily":150}
  ]
}
```

## 9. content_engine

**Output `data`**:
```json
{
  "tiktok_scripts": [...],
  "ugc_briefs": [...],
  "tweets": [...],
  "blog_posts": [{"title":"…","outline":[…],"h1":"…"}]
}
```

## 10. market_score

**Inputs**: outputs of agents 1–9

**Output `data`**:
```json
{
  "score": 82,
  "verdict": "GO",
  "subscores": {
    "demand": 9, "competition": 6, "branding": 8, "retention": 7,
    "ltv": 8, "virality": 9, "seo": 7, "ppc": 8, "scalability": 8,
    "technical_difficulty": 4
  },
  "risks": ["regulatory FDA labelling","CAC inflation Q4"],
  "next_actions": ["lock supplier","trademark search","build LP","run $500 test"]
}
```
