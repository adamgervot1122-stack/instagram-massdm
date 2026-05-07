import { mockDossier } from "@/lib/mock";

export default function RisksDashboard() {
  const ms = mockDossier.agents.market_score?.data;
  return (
    <div className="space-y-6">
      <header><h1 className="text-2xl font-semibold">Risks</h1></header>

      <div className="card">
        <h2 className="font-semibold">Top risks</h2>
        <ul className="mt-3 space-y-2 text-sm">
          {ms?.risks?.map((r: string) => (
            <li key={r} className="flex gap-2 rounded-lg border border-border bg-bg/40 p-3">
              <span className="text-rose-400">⚠</span>
              <span>{r}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
