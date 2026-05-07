import type { Dossier } from "./api";

// Used in v0.1 dashboards before the agents API is wired up.
export const mockDossier: Dossier = {
  niche: "non-melatonin sleep aid",
  geo: ["US", "UK", "DE", "FR", "BR"],
  score: 82,
  verdict: "GO",
  gated: false,
  cost_usd: 1.84,
  agents: {
    market_score: {
      status: "ok",
      cost_usd: 0.32,
      data: {
        score: 82,
        verdict: "GO",
        subscores: {
          demand: 9, competition: 6, branding_potential: 8, retention: 7,
          ltv: 8, virality: 9, seo: 7, ppc: 8, scalability_3y: 8,
          technical_difficulty: 4,
        },
        risks: [
          "FDA labelling for sleep claims",
          "CAC inflation in Q4 retail season",
          "supplier lead time on magnesium glycinate",
        ],
        next_actions: [
          "Lock supplier on 60-cap bottles",
          "Trademark search for 'NIGHTSHIFT'",
          "Build LP + run $500 test in US",
          "Cast 5 UGC creators (3am-waker archetype)",
          "Draft 10 TikTok scripts using verbatim Reddit pains",
        ],
        geo_ranking: [
          { country: "US", score: 86, tier: "TOP", cac_est: 18.4, cpm: 12.3 },
          { country: "DE", score: 71, tier: "BLUE_OCEAN", cac_est: 9.1, cpm: 7.2 },
          { country: "UK", score: 70, tier: "WATCH", cac_est: 11.2, cpm: 9.1 },
          { country: "BR", score: 48, tier: "WATCH", cac_est: 4.2, cpm: 3.1 },
          { country: "FR", score: 34, tier: "AVOID", reason: "regulated category" },
        ],
      },
    },
    trend_hunter: {
      status: "ok",
      cost_usd: 0.12,
      data: {
        trends: [
          { keyword: "magnesium glycinate sleep", velocity_30d: 1.42, saturation: 0.31, viral_score: 78, regions: ["US","CA","UK"] },
          { keyword: "non melatonin sleep aid", velocity_30d: 1.68, saturation: 0.22, viral_score: 84, regions: ["US"] },
          { keyword: "wake up 3am cant sleep", velocity_30d: 1.21, saturation: 0.18, viral_score: 71, regions: ["US","UK","DE"] },
        ],
      },
    },
    seo_hunter: {
      status: "ok",
      cost_usd: 0.18,
      data: {
        roi_score: 82,
        keywords: [
          { kw: "natural sleep aid no melatonin", volume: 12100, kd: 18, cpc: 1.84, intent: "commercial" },
          { kw: "best magnesium for sleep", volume: 49500, kd: 38, cpc: 2.10, intent: "commercial" },
          { kw: "wake up 3am every night", volume: 8100, kd: 12, cpc: 0.94, intent: "informational" },
          { kw: "sleep aid for adults 40s", volume: 3600, kd: 9, cpc: 1.42, intent: "commercial" },
        ],
      },
    },
    reddit_pain: {
      status: "ok",
      cost_usd: 0.21,
      data: {
        pains: [
          { theme: "wake up at 3am", frequency: 0.34, intensity: 0.81,
            verbatim: ["I literally wake up at 3am every. single. night.","Melatonin makes me feel drugged the next day"],
            subs: ["r/insomnia","r/Biohackers"] },
          { theme: "melatonin grogginess", frequency: 0.27, intensity: 0.68,
            verbatim: ["Melatonin gives me weird dreams and I'm hungover all morning"],
            subs: ["r/Supplements"] },
        ],
        emotional_register: ["frustrated","desperate","skeptical"],
      },
    },
    social_viral: {
      status: "ok",
      cost_usd: 0.18,
      data: {
        hooks: [
          { text: "POV: it's 3am and you're staring at the ceiling…", format: "talking-head + b-roll", avg_views: 1_200_000, hashtags: ["#cantsleep","#sleeptok"] },
          { text: "I tried every sleep aid. Only ONE worked.", format: "listicle", avg_views: 890_000, hashtags: ["#insomnia","#sleephack"] },
        ],
      },
    },
    competitor: {
      status: "ok",
      cost_usd: 0.24,
      data: {
        competitors: [
          { domain: "calm.com", traffic: 18_400_000, top_kw: ["sleep meditation"], pricing: { month: 14.99, year: 69.99 }, weaknesses: ["no science angle","poor mobile checkout"] },
          { domain: "olly.com", traffic: 1_200_000, top_kw: ["sleep gummies"], pricing: { month: 13.99 }, weaknesses: ["uses melatonin","kid-coded branding"] },
        ],
        gaps: ["no premium DTC product targeting non-melatonin users 30-45 USA"],
      },
    },
    offer_generator: {
      status: "ok",
      cost_usd: 0.18,
      data: {
        offer: {
          name: "NIGHTSHIFT",
          format: "60-capsule bottle, 30-day supply",
          price: { month: 39, trial: 19 },
          usp: "the only non-melatonin formula tested for 3am wake-ups",
          positioning: "premium DTC, science-led, anti-grogginess",
          emotional_angle: "finally sleep through the night without feeling drugged",
        },
      },
    },
    landing_page: { status: "ok", cost_usd: 0.21, data: { sections: [] } },
    ppc: { status: "ok", cost_usd: 0.12, data: { campaigns: [] } },
    content_engine: { status: "ok", cost_usd: 0.08, data: { tiktok_scripts: [] } },
  },
};
