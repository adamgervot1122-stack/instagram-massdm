import type { GeoTier } from "@/lib/api";
import { mockDossier } from "@/lib/mock";
import { cn } from "@/lib/cn";

const TIER_TONE: Record<GeoTier, string> = {
  TOP: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  BLUE_OCEAN: "bg-sky-500/15 text-sky-300 border-sky-500/30",
  WATCH: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  AVOID: "bg-rose-500/15 text-rose-300 border-rose-500/30",
};

export default function GeoDashboard() {
  const ranking = mockDossier.agents.market_score?.data?.geo_ranking ?? [];
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Geography</h1>
        <p className="text-sm text-text-muted">
          Per-country opportunity score, CPM, estimated CAC.
        </p>
      </header>

      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-text-muted">
            <tr>
              <th className="px-3 py-2 text-left">Country</th>
              <th className="px-3 py-2 text-right">Score</th>
              <th className="px-3 py-2 text-left">Tier</th>
              <th className="px-3 py-2 text-right">CPM</th>
              <th className="px-3 py-2 text-right">CAC est.</th>
              <th className="px-3 py-2 text-left">Note</th>
            </tr>
          </thead>
          <tbody>
            {ranking.map((g: any) => (
              <tr key={g.country} className="border-t border-border">
                <td className="px-3 py-2 font-medium">{g.country}</td>
                <td className="px-3 py-2 text-right">{g.score}</td>
                <td className="px-3 py-2">
                  <span className={cn(
                    "score-pill border",
                    TIER_TONE[g.tier as GeoTier],
                  )}>
                    {g.tier.replace("_", " ")}
                  </span>
                </td>
                <td className="px-3 py-2 text-right">${g.cpm?.toFixed(2) ?? "—"}</td>
                <td className="px-3 py-2 text-right">${g.cac_est?.toFixed(2) ?? "—"}</td>
                <td className="px-3 py-2 text-text-muted">{g.reason ?? ""}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
