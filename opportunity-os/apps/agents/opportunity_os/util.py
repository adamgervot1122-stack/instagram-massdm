"""Cross-agent helpers (shared cost + JSON parsing)."""

from __future__ import annotations

import json
from typing import Any

# Anthropic public per-M-token pricing (USD). Update when rates change.
MODEL_RATES: dict[str, tuple[float, float]] = {
    "claude-opus-4-7": (15.0, 75.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (0.8, 4.0),
}


def estimate_cost(usage: dict[str, int], model: str) -> float:
    in_per_m, out_per_m = MODEL_RATES.get(model, (3.0, 15.0))
    return (
        usage.get("input_tokens", 0) * in_per_m
        + usage.get("output_tokens", 0) * out_per_m
    ) / 1_000_000


def safe_json(text: str, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    """Lenient JSON parser — extracts the first {...} block."""
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {**(fallback or {}), "_raw": text}
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {**(fallback or {}), "_raw": text}
