import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="max-w-2xl text-center">
        <div className="mx-auto mb-6 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-accent to-accent2" />
        <h1 className="text-5xl font-bold tracking-tight">OPPORTUNITY OS</h1>
        <p className="mt-4 text-lg text-text-muted">
          Autonomous business-opportunity detection, scoring & launch platform.
          Thinks like a VC + hedge fund + DTC brand.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link
            href="/dashboard"
            className="rounded-xl bg-accent px-5 py-2.5 text-sm font-semibold text-bg hover:opacity-90"
          >
            Open dashboard
          </Link>
          <a
            href="https://github.com"
            className="rounded-xl border border-border px-5 py-2.5 text-sm font-semibold hover:bg-panel"
          >
            Docs
          </a>
        </div>
      </div>
    </main>
  );
}
