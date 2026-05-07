# Architecture

OPPORTUNITY OS is a **data-pipeline + multi-agent system** with a Next.js
front-office that surfaces opportunities, scores, and generated assets.

## Layers

### 1. Ingestion layer (Python)
- Scrapers (Playwright / Apify / BrightData)
- API clients (SEMrush, DataForSEO, Google Trends pytrends, Reddit PRAW,
  TikTok Creative Center, Meta Ads Library)
- Normalises raw payloads into the `signal` table

### 2. Agent layer (Python)
Each agent in `apps/agents/agents/<name>/` is an isolated module:

```
agents/<name>/
├── __init__.py
├── agent.py        # entrypoint: run(input) -> output
├── prompts/        # prompt templates (Jinja2)
├── schema.py       # pydantic IO contracts
└── tests/
```

Agents communicate via **typed pydantic models** persisted in
`agent_runs` (input, output, cost, latency, model used).

### 3. Orchestrator (Python)
`apps/agents/pipeline/orchestrator.py`. Runs the DAG:

```
trend_hunter ─┬─► seo_hunter ─┐
              ├─► reddit_pain ┤
              └─► social_viral┤
                              ├─► market_score ─► offer_generator ─► (landing_page, ppc, content_engine)
              competitor ─────┘
```

Concurrency where edges are independent (asyncio + semaphore).
Each step is **resumable** from `agent_runs` cache.

### 4. Storage
- **Postgres / Supabase** for relational data (Prisma schema)
- **S3 / Supabase Storage** for generated assets (HTML, MP4 storyboards, images)
- **Redis** for queue + idempotency keys

### 5. API
- Next.js Route Handlers (`apps/web/app/api/**`) for CRUD on opportunities
- A thin Python FastAPI sidecar (`apps/agents/api/`) exposes
  `/run/<agent>` and `/pipeline` for the web UI and for n8n / Make webhooks

### 6. Front-office (Next.js)
- `/dashboard/opportunities` — list + scoring grid
- `/dashboard/opportunities/[id]` — full dossier with the 9 sub-dashboards
- `/dashboard/runs` — agent-run telemetry (cost, latency, errors)
- `/dashboard/geo` — heatmap + GO/NO-GO per country

### 7. Automation
- **n8n** scenarios trigger the pipeline daily for a list of niches
- **Make / Zapier** push the dossier to Notion, Slack, email
- Stripe webhook → unlocks premium tiers

## Reliability

- All external calls retry with exponential backoff + jitter
- Agent outputs validated against pydantic schemas; failed runs are
  retried with a `repair` prompt up to 2× before being marked `failed`
- Idempotency: `(niche, geo, date)` is the natural key; reruns short-circuit
  on cache hit unless `--force`

## Cost controls

- Caching: SEO API responses cached 7 days, scraped pages 24h
- Prompt caching with Anthropic for the long synthesis prompts
- Hard daily $ ceiling per workspace, enforced in `pipeline/orchestrator.py`

## Security

- All third-party API keys live in Vault / Doppler, **never** in `.env` in repo
- Row-level security on Supabase: `workspace_id` scopes everything
- Outbound scraping respects robots.txt + per-domain rate limits
