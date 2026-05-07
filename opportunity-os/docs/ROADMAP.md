# Roadmap

## v0.1 — scaffold (this PR)
- Repo layout, docs, Prisma schema
- Agent skeletons with typed I/O
- Pipeline orchestrator
- Next.js dashboard shell with mock data

## v0.2 — first real pipeline
- Wire `trend_hunter` to pytrends
- Wire `seo_hunter` to DataForSEO
- Wire `reddit_pain` to PRAW
- Replace mock data in dashboards with live runs

## v0.3 — synthesis + scoring
- `competitor`, `market_score`, `offer_generator` end-to-end
- GO / NO-GO works on real data

## v0.4 — generation
- `landing_page` agent → renders to `/p/[slug]` Next.js route
- `ppc` + `content_engine` agents producing usable briefs
- Stripe-gated premium tier (full dossier export to Notion / PDF)

## v0.5 — automation
- n8n templates for daily niche scans
- Slack + email digest of new GO opportunities
- Webhook ingestion from Apify / BrightData

## v1.0 — launch
- Multi-workspace SaaS, RLS-isolated
- Public marketplace of validated opportunities
