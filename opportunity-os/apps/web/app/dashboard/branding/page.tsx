import { mockDossier } from "@/lib/mock";

export default function BrandingDashboard() {
  const offer = mockDossier.agents.offer_generator?.data?.offer;
  return (
    <div className="space-y-6">
      <header><h1 className="text-2xl font-semibold">Branding</h1></header>

      <div className="card">
        <p className="text-xs uppercase tracking-wider text-text-muted">Brand name</p>
        <h2 className="mt-1 text-4xl font-bold tracking-tight">{offer?.name}</h2>
        <p className="mt-3 max-w-2xl text-text-muted">{offer?.positioning}</p>

        <div className="mt-5 grid gap-3 md:grid-cols-3">
          <div className="rounded-xl border border-border bg-bg/40 p-4">
            <p className="text-xs text-text-muted">USP</p>
            <p className="mt-1 text-sm">{offer?.usp}</p>
          </div>
          <div className="rounded-xl border border-border bg-bg/40 p-4">
            <p className="text-xs text-text-muted">Emotional angle</p>
            <p className="mt-1 text-sm italic">"{offer?.emotional_angle}"</p>
          </div>
          <div className="rounded-xl border border-border bg-bg/40 p-4">
            <p className="text-xs text-text-muted">Format</p>
            <p className="mt-1 text-sm">{offer?.format}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
