import { mockDossier } from "@/lib/mock";

export default function SEODashboard() {
  const data = mockDossier.agents.seo_hunter?.data;
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">SEO</h1>
        <p className="text-sm text-text-muted">ROI score: {data?.roi_score}/100</p>
      </header>
      <div className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-text-muted">
            <tr>
              <th className="px-3 py-2 text-left">Keyword</th>
              <th className="px-3 py-2 text-right">Volume</th>
              <th className="px-3 py-2 text-right">KD</th>
              <th className="px-3 py-2 text-right">CPC</th>
              <th className="px-3 py-2 text-left">Intent</th>
            </tr>
          </thead>
          <tbody>
            {data?.keywords?.map((k: any) => (
              <tr key={k.kw} className="border-t border-border">
                <td className="px-3 py-2">{k.kw}</td>
                <td className="px-3 py-2 text-right">{k.volume.toLocaleString()}</td>
                <td className="px-3 py-2 text-right">{k.kd}</td>
                <td className="px-3 py-2 text-right">${k.cpc.toFixed(2)}</td>
                <td className="px-3 py-2">{k.intent}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
