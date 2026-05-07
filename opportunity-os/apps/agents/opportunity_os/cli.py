"""Command-line interface."""

from __future__ import annotations

import asyncio
import json
import sys

import click

from .pipeline import run_pipeline


@click.group()
def main() -> None:
    """OPPORTUNITY OS — agent CLI."""


@main.command()
@click.option("--niche", required=True, help="Niche to investigate.")
@click.option("--geo", default="US,UK,FR", help="Comma-separated ISO-3166 alpha-2 codes.")
@click.option("--period-days", default=90, type=int)
@click.option("--force", is_flag=True, help="Skip the score gate.")
@click.option("--out", type=click.Path(), help="Write dossier JSON to this path.")
def pipeline(niche: str, geo: str, period_days: int, force: bool, out: str | None) -> None:
    """Run the full pipeline and emit the dossier as JSON."""
    geos = [g.strip().upper() for g in geo.split(",") if g.strip()]
    dossier = asyncio.run(run_pipeline(niche, geos, period_days, force=force))
    text = json.dumps(dossier, indent=2, default=str)
    if out:
        with open(out, "w") as f:
            f.write(text)
        click.echo(f"Wrote dossier → {out}")
    else:
        click.echo(text)


@main.command()
@click.argument("agent_name")
@click.option("--niche", required=True)
@click.option("--geo", default="US")
def run(agent_name: str, niche: str, geo: str) -> None:
    """Run a single agent."""
    from .agents import REGISTRY
    from .types import AgentName, AgentRunInput

    try:
        name = AgentName(agent_name)
    except ValueError:
        click.echo(f"Unknown agent: {agent_name}", err=True)
        sys.exit(1)

    cls = REGISTRY[name]
    geos = [g.strip().upper() for g in geo.split(",")]
    output = asyncio.run(cls().run(AgentRunInput(niche=niche, geo=geos)))
    click.echo(json.dumps(output.model_dump(), indent=2, default=str))


if __name__ == "__main__":
    main()
