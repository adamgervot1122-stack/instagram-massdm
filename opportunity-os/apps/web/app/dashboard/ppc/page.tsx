import { mockDossier } from "@/lib/mock";

export default function PPCDashboard() {
  const data = mockDossier.agents.ppc?.data;
  const subs = mockDossier.agents.market_score?.data?.subscores ?? {};
  return (
    <div className="space-y-6">
      <header><h1 className="text-2xl font-semibold">PPC</h1></header>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-3">
        <Kpi label="PPC score" value={`${subs.ppc ?? 0}/10`} />
        <Kpi label="Virality score" value={`${subs.virality ?? 0}/10`} />
        <Kpi label="Daily test budget" value="$500" />
      </section>

      {data?.campaigns?.length ? (
        <div className="card space-y-4">
          {data.campaigns.map((c: any) => (
            <div key={`${c.platform}-${c.objective}`} className="rounded-xl border border-border p-3">
              <p className="font-semibold capitalize">{c.platform} · {c.objective}</p>
              <p className="text-xs text-text-muted">budget: ${c.budget_daily}/d</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-sm text-text-muted">
          Run the pipeline to generate campaign briefs (Meta / TikTok / Google).
        </div>
      )}
    </div>
  );
}

function Kpi({ label, value }: { label: string; value: string }) {
  return (
    <div className="kpi">
      <p className="text-xs uppercase tracking-wider text-text-muted">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}
