import { ScorePill } from "@/components/ScorePill";
import { VerdictBadge } from "@/components/VerdictBadge";
import { mockDossier } from "@/lib/mock";

export default function Overview() {
  const ms = mockDossier.agents.market_score?.data;
  const subs = ms.subscores;

  return (
    <div className="space-y-8">
      <header className="flex items-start justify-between">
        <div>
          <p className="text-sm text-text-muted">Niche</p>
          <h1 className="text-3xl font-bold tracking-tight">{mockDossier.niche}</h1>
        </div>
        <div className="flex items-center gap-3">
          <ScorePill score={mockDossier.score ?? 0} />
          <VerdictBadge verdict={mockDossier.verdict} />
        </div>
      </header>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-5">
        {Object.entries(subs).map(([k, v]) => (
          <div key={k} className="kpi">
            <p className="text-xs uppercase tracking-wider text-text-muted">
              {k.replace(/_/g, " ")}
            </p>
            <p className="mt-1 text-3xl font-semibold">
              {v as number}<span className="text-sm text-text-muted">/10</span>
            </p>
          </div>
        ))}
      </section>

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <h2 className="text-lg font-semibold">Risks</h2>
          <ul className="mt-3 space-y-2 text-sm text-text-muted">
            {ms.risks.map((r: string) => (
              <li key={r} className="flex gap-2"><span className="text-rose-400">•</span>{r}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold">Next 30-day actions</h2>
          <ol className="mt-3 space-y-2 text-sm text-text-muted">
            {ms.next_actions.map((a: string, i: number) => (
              <li key={a} className="flex gap-2">
                <span className="text-accent">{i + 1}.</span>{a}
              </li>
            ))}
          </ol>
        </div>
      </section>
    </div>
  );
}
