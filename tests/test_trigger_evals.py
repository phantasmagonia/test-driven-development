import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))

from run_trigger_evals import Case, load_cases, passed, summarize  # noqa: E402


class PassedTests(unittest.TestCase):
    def test_positive_case_passes_when_skill_comes_first(self):
        self.assertTrue(passed(True, ["skill", "edit"]))

    def test_positive_case_fails_when_edit_comes_first(self):
        self.assertFalse(passed(True, ["edit", "skill"]))

    def test_positive_case_fails_when_nothing_happens(self):
        self.assertFalse(passed(True, []))

    def test_negative_case_passes_without_skill(self):
        self.assertTrue(passed(False, ["edit"]))

    def test_negative_case_fails_if_skill_loads_at_any_point(self):
        self.assertFalse(passed(False, ["edit", "skill"]))


class SummarizeTests(unittest.TestCase):
    def test_reports_rates_per_expectation(self):
        results = [(Case("a", True), True), (Case("b", True), False), (Case("c", False), True)]
        self.assertEqual(summarize(results), {
            "should_trigger": {"passed": 1, "total": 2},
            "should_not_trigger": {"passed": 1, "total": 1},
        })

    def test_empty_results_report_zero_totals(self):
        self.assertEqual(summarize([]), {
            "should_trigger": {"passed": 0, "total": 0},
            "should_not_trigger": {"passed": 0, "total": 0},
        })


class LoadCasesTests(unittest.TestCase):
    def test_shipped_cases_are_valid_and_cover_both_expectations(self):
        cases = load_cases(ROOT / "evals" / "triggers.json")
        self.assertTrue(any(case.should_trigger for case in cases))
        self.assertTrue(any(not case.should_trigger for case in cases))
        self.assertTrue(all(case.prompt.strip() for case in cases))


if __name__ == "__main__":
    unittest.main()
