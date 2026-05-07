import { mockDossier } from "@/lib/mock";

export default function CompetitorsDashboard() {
  const data = mockDossier.agents.competitor?.data;
  return (
    <div className="space-y-6">
      <header><h1 className="text-2xl font-semibold">Competitors</h1></header>

      <div className="grid gap-4 md:grid-cols-2">
        {data?.competitors?.map((c: any) => (
          <div key={c.domain} className="card">
            <div className="flex items-start justify-between">
              <h2 className="text-lg font-semibold">{c.domain}</h2>
              <p className="text-xs text-text-muted">
                {c.traffic.toLocaleString()} mo. visits
              </p>
            </div>
            <p className="mt-1 text-xs text-text-muted">
              top kw: {c.top_kw.join(", ")}
            </p>
            <p className="mt-2 text-sm">
              ${Object.entries(c.pricing).map(([k, v]) => `${v}/${k}`).join(" · ")}
            </p>
            <div className="mt-3">
              <p className="text-xs uppercase tracking-wider text-text-muted">Weaknesses</p>
              <ul className="mt-1 space-y-1 text-sm text-text-muted">
                {c.weaknesses.map((w: string) => (
                  <li key={w}>• {w}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2 className="font-semibold">Market gaps</h2>
        <ul className="mt-3 space-y-2 text-sm text-text-muted">
          {data?.gaps?.map((g: string) => (
            <li key={g} className="flex gap-2"><span className="text-accent">→</span>{g}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
