import Link from "next/link";
import {
  LayoutDashboard, TrendingUp, Search, MessageSquare, Sparkles,
  Building2, DollarSign, Globe2, Megaphone, Palette, AlertTriangle,
} from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/dashboard/opportunity", label: "Opportunity", icon: Sparkles },
  { href: "/dashboard/seo", label: "SEO", icon: Search },
  { href: "/dashboard/social", label: "Social / Viral", icon: TrendingUp },
  { href: "/dashboard/pain", label: "Pain points", icon: MessageSquare },
  { href: "/dashboard/competitors", label: "Competitors", icon: Building2 },
  { href: "/dashboard/monetization", label: "Monetisation", icon: DollarSign },
  { href: "/dashboard/geo", label: "Geography", icon: Globe2 },
  { href: "/dashboard/ppc", label: "PPC", icon: Megaphone },
  { href: "/dashboard/branding", label: "Branding", icon: Palette },
  { href: "/dashboard/risks", label: "Risks", icon: AlertTriangle },
];

export function Sidebar() {
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-border bg-panel/60">
      <div className="px-5 py-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="h-8 w-8 rounded-lg bg-gradient-to-br from-accent to-accent2" />
          <span className="font-semibold tracking-tight">OPPORTUNITY OS</span>
        </Link>
      </div>
      <nav className="flex-1 space-y-0.5 px-3">
        {NAV.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href as any}
            className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-text-muted hover:bg-border/40 hover:text-text"
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
      </nav>
      <div className="px-5 py-4 text-xs text-text-muted">v0.1 — scaffold</div>
    </aside>
  );
}
