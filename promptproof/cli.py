"""Command line interface: python -m promptproof <command> ..."""
from __future__ import annotations

import argparse
import json
import sys

from .models import find_duplicates, load_shots
from .planner import build_plan, savings_vs_direct, to_csv, to_markdown_checklist
from .prompt import compose_prompt


def _load_rates(path: str | None) -> dict | None:
    if not path:
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="promptproof",
        description="Structure video prompts, proof cheaply, finish only approved shots.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="validate a shots JSON file")
    p_validate.add_argument("input")

    p_prompt = sub.add_parser("prompt", help="print the composed prompt for one shot id")
    p_prompt.add_argument("input")
    p_prompt.add_argument("shot_id")

    p_plan = sub.add_parser("plan", help="build a two-stage proof/final plan")
    p_plan.add_argument("input")
    p_plan.add_argument("--approve", default="",
                        help="comma-separated shot ids approved for final render")
    p_plan.add_argument("--rates", default=None, help="JSON file with per-second rates")
    p_plan.add_argument("--format", choices=("md", "csv"), default="md")
    p_plan.add_argument("--out", default=None, help="write to file instead of stdout")

    args = parser.parse_args(argv)
    shots = load_shots(args.input)

    if args.command == "validate":
        problems: list[str] = []
        for shot in shots:
            problems.extend(shot.validate())
        for fp, ids in find_duplicates(shots).items():
            problems.append(f"duplicate content {fp}: {', '.join(ids)}")
        if problems:
            print("\n".join(problems))
            return 1
        print(f"OK: {len(shots)} shot(s), no problems found")
        return 0

    if args.command == "prompt":
        for shot in shots:
            if shot.id == args.shot_id:
                print(compose_prompt(shot))
                return 0
        print(f"shot id not found: {args.shot_id}", file=sys.stderr)
        return 2

    if args.command == "plan":
        approved = {s.strip() for s in args.approve.split(",") if s.strip()}
        rates = _load_rates(args.rates)
        plan = build_plan(shots, approved_ids=approved, rates=rates)
        text = to_markdown_checklist(plan) if args.format == "md" else to_csv(plan)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"wrote {args.out}: proof CNY {plan.proof_cost:.2f}, "
                  f"final CNY {plan.final_cost:.2f}, "
                  f"savings vs direct CNY {savings_vs_direct(plan, shots, rates):.2f}")
        else:
            print(text, end="")
        return 0

    return 2  # pragma: no cover


if __name__ == "__main__":
    raise SystemExit(main())
