import { NextRequest, NextResponse } from "next/server";
import { runPipeline } from "@/lib/api";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const body = await req.json();
  if (!body?.niche || !Array.isArray(body?.geo)) {
    return NextResponse.json(
      { error: "niche and geo[] are required" },
      { status: 400 },
    );
  }
  try {
    const dossier = await runPipeline(body);
    return NextResponse.json(dossier);
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 502 });
  }
}
