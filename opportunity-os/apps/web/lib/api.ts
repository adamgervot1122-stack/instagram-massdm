// Thin client for the Python agents API (FastAPI sidecar).

const BASE = process.env.AGENTS_API_URL || "http://localhost:8000";

export type Verdict = "GO" | "GO_WITH_RESERVES" | "NO_GO_NOW" | "NO_GO";
export type GeoTier = "TOP" | "BLUE_OCEAN" | "WATCH" | "AVOID";

export interface GeoScore {
  country: string;
  score: number;
  tier: GeoTier;
  cac_est?: number;
  cpm?: number;
  reason?: string;
}

export interface Subscores {
  demand: number;
  competition: number;
  branding_potential: number;
  retention: number;
  ltv: number;
  virality: number;
  seo: number;
  ppc: number;
  scalability_3y: number;
  technical_difficulty: number;
}

export interface Dossier {
  niche: string;
  geo: string[];
  score: number | null;
  verdict: Verdict;
  gated: boolean;
  cost_usd: number;
  agents: Record<string, { data: any; status: string; cost_usd: number }>;
}

export async function runPipeline(input: {
  niche: string;
  geo: string[];
  period_days?: number;
  force?: boolean;
}): Promise<Dossier> {
  const res = await fetch(`${BASE}/pipeline`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`pipeline failed: ${res.status}`);
  return res.json();
}
