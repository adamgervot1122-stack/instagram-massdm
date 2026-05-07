import { cn } from "@/lib/cn";

interface Props {
  score: number;
  className?: string;
}

export function ScorePill({ score, className }: Props) {
  const tone =
    score >= 75 ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
    : score >= 60 ? "bg-amber-500/15 text-amber-300 border-amber-500/30"
    : score >= 45 ? "bg-orange-500/15 text-orange-300 border-orange-500/30"
    : "bg-rose-500/15 text-rose-300 border-rose-500/30";
  return (
    <span className={cn("score-pill border", tone, className)}>{score}/100</span>
  );
}
