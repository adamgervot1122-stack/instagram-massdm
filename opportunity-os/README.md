# OPPORTUNITY OS

> Autonomous business-opportunity detection & launch platform.
> Thinks like a VC + hedge fund + DTC brand + elite growth hacker + $100M SaaS founder.

OPPORTUNITY OS scans real-world demand signals (Google Trends, TikTok, Reddit,
SEMrush, Meta Ads Library, Amazon, etc.), extracts pain points, scores
opportunities, generates an offer + landing page + ad creatives + UGC scripts +
go-to-market plan, and outputs a GO / NO-GO verdict per geography.

---

## High-level pipeline

```
Google Trends
   │
   ▼
TikTok Trends ──► Reddit Pain Signals ──► SEO / Keyword Mining
                                                │
                                                ▼
                                       Competitor Analysis
                                                │
                                                ▼
                                         AI Synthesis Layer
                                                │
                                                ▼
                                       Opportunity Score (/100)
                                                │
                ┌───────────────┬────────────────┼────────────────┬────────────────┐
                ▼               ▼                ▼                ▼                ▼
          Offer Gen      Landing Page         Ads Gen       Content Engine   Geo Analyzer
                                                │
                                                ▼
                                          Master Dashboard
```

---

## Repo layout

```
opportunity-os/
├── apps/
│   ├── web/          # Next.js 14 + Tailwind + ShadCN dashboards
│   └── agents/       # Python AI agents (CrewAI / LangChain / Anthropic SDK)
├── packages/
│   └── shared/       # TypeScript shared types + zod schemas
├── prisma/
│   └── schema.prisma # PostgreSQL / Supabase schema
├── infra/
│   ├── docker-compose.yml
│   └── Makefile
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENTS.md
│   ├── PIPELINE.md
│   ├── SCORING.md
│   ├── GEO.md
│   └── ROADMAP.md
└── README.md
```

---

## The 10 agents

| # | Agent | Mission |
|---|---|---|
| 1 | `trend_hunter` | Google Trends, micro-trend velocity, saturation |
| 2 | `seo_hunter` | SEMrush / Ubersuggest / DataForSEO keyword mining |
| 3 | `reddit_pain` | Reddit + forums frustration + emotional language extraction |
| 4 | `social_viral` | TikTok / Reels hook + format mining |
| 5 | `competitor` | Competitor traffic, pricing, USP gaps |
| 6 | `offer_generator` | Synthesises an offer, USP, pricing |
| 7 | `landing_page` | Generates a full conversion-optimised landing page |
| 8 | `ppc` | Meta / TikTok / Google campaign briefs + audiences + creatives |
| 9 | `content_engine` | TikTok scripts, UGC, tweets, SEO blog posts |
| 10 | `market_score` | /100 score + GO / NO-GO verdict |

See [`docs/AGENTS.md`](./docs/AGENTS.md) for I/O contracts.

---

## Tech stack

- **Frontend**: Next.js 14, Tailwind, ShadCN, Framer Motion, Recharts
- **Backend / DB**: Supabase, PostgreSQL, Prisma
- **AI**: Anthropic Claude (Opus 4.7 / Sonnet 4.6), OpenAI, LangChain, CrewAI
- **Scraping**: Apify, BrightData, Playwright
- **SEO data**: SEMrush API, DataForSEO, Ahrefs MCP
- **Automation**: n8n, Make, Zapier
- **Hosting**: Vercel + Railway (agents)
- **Payments**: Stripe
- **Analytics**: PostHog, GA4

---

## Quickstart

```bash
# 1. Bootstrap
cp .env.example .env
make install

# 2. Database
make db-up
pnpm prisma migrate dev

# 3. Run a full pipeline (CLI)
make pipeline NICHE="sleep optimisation" GEO="US,UK,FR"

# 4. Frontend
make web
# → http://localhost:3000
```

---

## Output (per opportunity)

Every successful run produces a single JSON dossier + rendered dashboards:

1. Opportunity summary
2. ICP (ideal customer profile)
3. Pain points + verbatim user language
4. SEO keywords + difficulty + CPC
5. TikTok hooks + viral formats
6. Brand angle + tone of voice
7. Offer + pricing
8. Landing page (HTML + JSX)
9. UGC scripts (×5)
10. Meta + TikTok + Google ad briefs
11. Acquisition plan
12. Scaling plan (90 days)
13. Tech stack recommendation
14. Multi-agent architecture
15. Automations (n8n / Make scenarios)
16. MVP roadmap
17. KPI targets
18. Risks
19. Geographic ranking (TOP / BLUE OCEAN / AVOID)
20. **GO / NO-GO verdict**

---

## Status

Scaffold v0.1. See `docs/ROADMAP.md`.
