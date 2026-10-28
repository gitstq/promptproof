"""Cost estimation.

Rates are *configuration, not truth*: every provider prices differently
and prices change. The defaults below are worked examples only --
edit them in your own config file before trusting a total.
"""
from __future__ import annotations

# Example rates in CNY per second of generated video.
DEFAULT_RATES_CNY_PER_SEC = {
    "768P": 0.20,
    "1080P": 0.40,
    "2K": 0.80,
}

PROOF_RESOLUTION = "768P"


def estimate_cost(duration_sec: float, resolution: str,
                  rates: dict | None = None) -> float:
    """Cost of one render: duration x per-second rate for the resolution."""
    table = rates or DEFAULT_RATES_CNY_PER_SEC
    if resolution not in table:
        raise ValueError(f"no rate configured for resolution {resolution!r}")
    return round(float(duration_sec) * float(table[resolution]), 4)
