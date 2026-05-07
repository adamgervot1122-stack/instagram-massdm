import type { Verdict } from "@/lib/api";
import { cn } from "@/lib/cn";

const TONE: Record<Verdict, string> = {
  GO: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
  GO_WITH_RESERVES: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  NO_GO_NOW: "bg-orange-500/15 text-orange-300 border-orange-500/30",
  NO_GO: "bg-rose-500/15 text-rose-300 border-rose-500/30",
};

export function VerdictBadge({ verdict }: { verdict: Verdict }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wider",
        TONE[verdict],
      )}
    >
      {verdict.replace(/_/g, " ")}
    </span>
  );
}
