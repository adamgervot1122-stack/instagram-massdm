import { ScorePill } from "@/components/ScorePill";
import { VerdictBadge } from "@/components/VerdictBadge";
import { mockDossier } from "@/lib/mock";

export default function OpportunityDashboard() {
  const offer = mockDossier.agents.offer_generator?.data?.offer;
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Opportunity</h1>
        <div className="flex gap-3">
          <ScorePill score={mockDossier.score ?? 0} />
          <VerdictBadge verdict={mockDossier.verdict} />
        </div>
      </header>

      <div className="card">
        <p className="text-sm text-text-muted">Generated offer</p>
        <h2 className="mt-1 text-3xl font-bold">{offer?.name}</h2>
        <p className="mt-2 max-w-2xl text-text-muted">{offer?.usp}</p>

        <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
          <Field label="Format" value={offer?.format} />
          <Field label="Trial" value={`$${offer?.price?.trial}`} />
          <Field label="Monthly" value={`$${offer?.price?.month}`} />
          <Field label="Positioning" value={offer?.positioning} />
        </div>

        <div className="mt-5 rounded-xl border border-border bg-bg/40 p-4">
          <p className="text-xs uppercase tracking-wider text-text-muted">Emotional angle</p>
          <p className="mt-1 italic">"{offer?.emotional_angle}"</p>
        </div>
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: any }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wider text-text-muted">{label}</p>
      <p className="mt-1 font-medium">{value ?? "—"}</p>
    </div>
  );
}
