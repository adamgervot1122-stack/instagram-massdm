# Pipeline

The orchestrator runs a DAG of agents. Each node is a typed Python coroutine.

## DAG

```
                     ┌─────────────────┐
                     │  trend_hunter   │
                     └────────┬────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
   │   seo_hunter   │ │  reddit_pain   │ │  social_viral  │
   └────────┬───────┘ └────────┬───────┘ └────────┬───────┘
            └─────────────────┬┴─────────────────┘
                              ▼
                    ┌──────────────────┐
                    │    competitor    │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │   market_score   │  ← gate: if score < 60 → STOP
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ offer_generator  │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
   │ landing_page │ │     ppc      │ │  content_engine  │
   └──────────────┘ └──────────────┘ └──────────────────┘
```

## Gating

`market_score` is the **gate**. If `score < 60`, the pipeline short-circuits
and emits `verdict: NO_GO` — saving cost on offer + landing + ads generation.

Override with `--force` (CLI) or `force=true` (HTTP).

## Concurrency

- Layer 1 (`trend_hunter`) — single
- Layer 2 (`seo_hunter`, `reddit_pain`, `social_viral`) — `asyncio.gather`
- Layer 3 (`competitor`) — single, depends on layer 2 outputs
- Layer 4 (`market_score`) — single
- Layer 5 (`offer_generator`) — single
- Layer 6 (`landing_page`, `ppc`, `content_engine`) — `asyncio.gather`

## Resumability

Every node writes its output to the `agent_runs` table keyed by
`(workspace_id, niche, geo_set, period_days, agent_name, prompt_hash)`.

Re-running the pipeline with the same inputs short-circuits each node
that already has a successful run within `cache_ttl_hours` (default 24).

## Failure semantics

- Each agent has 2 automatic retries (exp. backoff)
- Failure of a non-critical leaf (e.g. `content_engine`) is logged but
  doesn't fail the pipeline — final dossier is marked `partial`
- Failure of a critical node (`market_score`, `offer_generator`) fails
  the pipeline; partial outputs are still persisted for inspection

## Telemetry

Each run emits:
- structured logs (JSON, shipped to Loki)
- OpenTelemetry traces (one root span per pipeline, child per agent)
- per-agent cost + token + latency metrics → Postgres + Grafana

## Triggering

| Trigger | Source |
|---|---|
| Manual | `make pipeline` CLI or `/dashboard/run` button |
| Scheduled | n8n cron, daily 03:00 UTC, per niche list |
| Webhook | `POST /api/pipeline` from Make / Zapier |
