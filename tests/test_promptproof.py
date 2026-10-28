"""Unit tests (standard-library unittest, no extra dependency needed).

Run:  python -m unittest discover -s tests -v
  or: python -m pytest tests/ -q   (if pytest is installed)
"""
import unittest

from promptproof.cost import estimate_cost
from promptproof.models import Shot, find_duplicates
from promptproof.planner import build_plan, savings_vs_direct, to_csv, to_markdown_checklist
from promptproof.prompt import compose_prompt


def make_shot(**overrides):
    base = dict(id="s1", subject="an orange cat at a desk",
                action="turns its head and blinks", camera="slow push-in",
                style="warm light", duration_sec=5.0, final_resolution="2K")
    base.update(overrides)
    return Shot(**base)


class TestPromptAndValidation(unittest.TestCase):
    def test_compose_prompt_has_labelled_sections(self):
        text = compose_prompt(make_shot())
        self.assertIn("[Subject] an orange cat at a desk", text)
        self.assertIn("[Action] turns its head and blinks", text)
        self.assertIn("[Camera] slow push-in", text)

    def test_validate_flags_empty_subject_and_bad_duration(self):
        problems = make_shot(subject="", duration_sec=99).validate()
        self.assertTrue(any("subject" in p for p in problems))
        self.assertTrue(any("duration" in p for p in problems))

    def test_validate_accepts_a_good_shot(self):
        self.assertEqual(make_shot().validate(), [])


class TestCost(unittest.TestCase):
    def test_estimate_cost_multiplies_duration_by_rate(self):
        # Default example rate for 2K is 0.80 CNY/sec.
        self.assertEqual(estimate_cost(5.0, "2K"), 4.0)
        self.assertEqual(estimate_cost(5.0, "768P"), 1.0)

    def test_estimate_cost_rejects_unknown_resolution(self):
        with self.assertRaises(ValueError):
            estimate_cost(5.0, "8K")


class TestPlanner(unittest.TestCase):
    def test_duplicates_are_detected_and_skipped_once(self):
        shots = [make_shot(), make_shot(id="s2")]
        self.assertEqual(len(find_duplicates(shots)), 1)
        plan = build_plan(shots)
        self.assertEqual(plan.skipped_duplicates, ["s2"])
        self.assertEqual(len([i for i in plan.items if i.stage == "proof"]), 1)

    def test_final_stage_only_contains_approved_shots(self):
        shots = [make_shot(), make_shot(id="s2", subject="a harbour at dawn",
                                         action="waves roll in")]
        plan = build_plan(shots, approved_ids={"s2"})
        finals = [i.shot_id for i in plan.items if i.stage == "final"]
        self.assertEqual(finals, ["s2"])
        self.assertEqual(plan.final_cost, 4.0)   # 5s x 0.80
        self.assertEqual(plan.proof_cost, 2.0)   # 2 proofs x 5s x 0.20

    def test_rejecting_an_expensive_shot_saves_money(self):
        shots = [make_shot(),
                 make_shot(id="s2", subject="a harbour at dawn",
                           action="waves roll in", duration_sec=10.0)]
        plan = build_plan(shots, approved_ids={"s1"})
        # Direct: 4.0 + 8.0 = 12.0; plan: proofs 1.0+2.0, final 4.0 = 7.0
        self.assertEqual(savings_vs_direct(plan, shots), 5.0)

    def test_exports_contain_checkboxes_and_csv_rows(self):
        plan = build_plan([make_shot()], approved_ids={"s1"})
        self.assertIn("- [ ] s1", to_markdown_checklist(plan))
        self.assertIn("s1,final,2K", to_csv(plan))


if __name__ == "__main__":
    unittest.main()
