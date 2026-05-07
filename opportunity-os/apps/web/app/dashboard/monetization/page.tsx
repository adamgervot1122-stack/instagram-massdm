import { mockDossier } from "@/lib/mock";

export default function MonetizationDashboard() {
  const offer = mockDossier.agents.offer_generator?.data?.offer;
  const subs = mockDossier.agents.market_score?.data?.subscores ?? {};
  return (
    <div className="space-y-6">
      <header><h1 className="text-2xl font-semibold">Monetisation</h1></header>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <Stat label="Trial" value={`$${offer?.price?.trial}`} />
        <Stat label="Monthly" value={`$${offer?.price?.month}`} />
        <Stat label="LTV score" value={`${subs.ltv ?? 0}/10`} />
        <Stat label="Retention score" value={`${subs.retention ?? 0}/10`} />
      </section>

      <div className="card">
        <h2 className="font-semibold">USP</h2>
        <p className="mt-1 text-text-muted">{offer?.usp}</p>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="kpi">
      <p className="text-xs uppercase tracking-wider text-text-muted">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}
