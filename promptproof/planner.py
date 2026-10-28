"""Two-stage planning: proof everything cheaply, finish only approved.

This is the core idea of PromptProof. Rendering every idea straight to
final quality wastes money on shots that a cheap proof would have
rejected in seconds. The planner therefore emits:

* Stage 1 (proof)  -- every unique, valid shot at 768P
* Stage 2 (final)  -- only the shots the user approved, at final quality

and reports how much that saves versus rendering everything at final
quality directly.
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field

from .cost import PROOF_RESOLUTION, estimate_cost
from .models import Shot, find_duplicates
from .prompt import compose_prompt


@dataclass
class PlanItem:
    shot_id: str
    stage: str  # "proof" or "final"
    resolution: str
    duration_sec: float
    cost_cny: float
    prompt: str


@dataclass
class Plan:
    items: list[PlanItem] = field(default_factory=list)
    skipped_duplicates: list[str] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)

    @property
    def proof_cost(self) -> float:
        return round(sum(i.cost_cny for i in self.items if i.stage == "proof"), 4)

    @property
    def final_cost(self) -> float:
        return round(sum(i.cost_cny for i in self.items if i.stage == "final"), 4)

    @property
    def total_cost(self) -> float:
        return round(self.proof_cost + self.final_cost, 4)


def build_plan(shots: list[Shot], approved_ids: set[str] | None = None,
               rates: dict | None = None) -> Plan:
    approved = approved_ids or set()
    plan = Plan()
    seen: set[str] = set()
    for shot in shots:
        problems = shot.validate()
        if problems:
            plan.invalid.extend(problems)
            continue
        fp = shot.fingerprint()
        if fp in seen:
            plan.skipped_duplicates.append(shot.id)
            continue
        seen.add(fp)
        prompt_text = compose_prompt(shot)
        plan.items.append(PlanItem(
            shot_id=shot.id, stage="proof", resolution=PROOF_RESOLUTION,
            duration_sec=float(shot.duration_sec),
            cost_cny=estimate_cost(shot.duration_sec, PROOF_RESOLUTION, rates),
            prompt=prompt_text,
        ))
        if shot.id in approved:
            plan.items.append(PlanItem(
                shot_id=shot.id, stage="final",
                resolution=shot.final_resolution,
                duration_sec=float(shot.duration_sec),
                cost_cny=estimate_cost(shot.duration_sec, shot.final_resolution, rates),
                prompt=prompt_text,
            ))
    return plan


def direct_final_cost(shots: list[Shot], rates: dict | None = None) -> float:
    """What it would cost to render every unique valid shot at final quality."""
    total = 0.0
    seen: set[str] = set()
    for shot in shots:
        if shot.validate():
            continue
        fp = shot.fingerprint()
        if fp in seen:
            continue
        seen.add(fp)
        total += estimate_cost(shot.duration_sec, shot.final_resolution, rates)
    return round(total, 4)


def savings_vs_direct(plan: Plan, shots: list[Shot],
                      rates: dict | None = None) -> float:
    """Money saved versus rendering every shot directly at final quality.

    Positive when rejected shots save more than the proofs cost.
    Negative when everything is approved: then the proofs are an extra
    (deliberate) quality-check cost on top of the final renders.
    """
    return round(direct_final_cost(shots, rates) - plan.total_cost, 4)


def to_markdown_checklist(plan: Plan) -> str:
    lines = ["# PromptProof task checklist", ""]
    for stage, title in (("proof", "Stage 1 - Proof (768P, check first)"),
                         ("final", "Stage 2 - Final (approved only)")):
        lines += [f"## {title}", ""]
        stage_items = [i for i in plan.items if i.stage == stage]
        if not stage_items:
            lines.append("_none_")
        for item in stage_items:
            lines.append(
                f"- [ ] {item.shot_id} | {item.resolution} | "
                f"{item.duration_sec:g}s | CNY {item.cost_cny:.2f}"
            )
            lines.append("  ```text")
            lines.extend(f"  {ln}" for ln in item.prompt.splitlines())
            lines.append("  ```")
        lines.append("")
    lines.append(f"Proof cost: CNY {plan.proof_cost:.2f}  ")
    lines.append(f"Final cost: CNY {plan.final_cost:.2f}  ")
    lines.append(f"Planned total: CNY {plan.total_cost:.2f}")
    if plan.skipped_duplicates:
        lines.append(f"\nSkipped duplicates: {', '.join(plan.skipped_duplicates)}")
    if plan.invalid:
        lines.append("\nInvalid shots:")
        lines.extend(f"- {p}" for p in plan.invalid)
    return "\n".join(lines) + "\n"


def to_csv(plan: Plan) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["shot_id", "stage", "resolution", "duration_sec", "cost_cny"])
    for item in plan.items:
        writer.writerow([item.shot_id, item.stage, item.resolution,
                         item.duration_sec, f"{item.cost_cny:.2f}"])
    return buf.getvalue()
