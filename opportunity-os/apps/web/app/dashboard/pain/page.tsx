import { mockDossier } from "@/lib/mock";

export default function PainDashboard() {
  const data = mockDossier.agents.reddit_pain?.data;
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Pain points</h1>
        <p className="text-sm text-text-muted">
          Emotional register: {data?.emotional_register?.join(" · ")}
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        {data?.pains?.map((p: any) => (
          <div key={p.theme} className="card">
            <div className="flex items-start justify-between">
              <h2 className="text-lg font-semibold">{p.theme}</h2>
              <div className="text-right text-xs text-text-muted">
                <p>freq {Math.round(p.frequency * 100)}%</p>
                <p>intensity {Math.round(p.intensity * 100)}%</p>
              </div>
            </div>
            <ul className="mt-3 space-y-2">
              {p.verbatim.map((v: string) => (
                <li key={v} className="rounded-lg border border-border bg-bg/40 p-3 italic text-text-muted">
                  "{v}"
                </li>
              ))}
            </ul>
            <p className="mt-3 text-xs text-text-muted">{p.subs.join(" · ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
