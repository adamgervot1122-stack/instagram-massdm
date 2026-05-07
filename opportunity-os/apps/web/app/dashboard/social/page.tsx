import { mockDossier } from "@/lib/mock";

export default function SocialDashboard() {
  const trends = mockDossier.agents.trend_hunter?.data?.trends ?? [];
  const hooks = mockDossier.agents.social_viral?.data?.hooks ?? [];
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Social / Viral</h1>
      </header>

      <section className="card">
        <h2 className="font-semibold">Emerging trends</h2>
        <div className="mt-3 grid gap-3 md:grid-cols-3">
          {trends.map((t: any) => (
            <div key={t.keyword} className="kpi">
              <p className="font-medium">{t.keyword}</p>
              <p className="mt-1 text-xs text-text-muted">
                velocity ×{t.velocity_30d.toFixed(2)} · viral {t.viral_score}/100
              </p>
              <p className="mt-1 text-xs text-text-muted">{t.regions.join(", ")}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h2 className="font-semibold">Top viral hooks</h2>
        <ul className="mt-3 space-y-3">
          {hooks.map((h: any) => (
            <li key={h.text} className="rounded-xl border border-border bg-bg/40 p-3">
              <p className="font-medium">"{h.text}"</p>
              <p className="mt-1 text-xs text-text-muted">
                {h.format} · ~{(h.avg_views / 1_000_000).toFixed(1)}M views ·{" "}
                {h.hashtags.join(" ")}
              </p>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
