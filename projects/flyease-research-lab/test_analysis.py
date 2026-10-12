import unittest
from analysis import generate_synthetic_survey, evaluate

class FlyEaseTests(unittest.TestCase):
    def test_seed_reproducible(self):
        self.assertTrue(generate_synthetic_survey(80).equals(generate_synthetic_survey(80)))
    def test_satisfaction_bounds(self):
        self.assertTrue(generate_synthetic_survey(80).satisfaction.between(1, 5).all())
    def test_baseline_comparison(self):
        report = evaluate(generate_synthetic_survey(500))
        self.assertLess(report["ridge_mae"], report["baseline_mae"])
        self.assertEqual(report["holdout_responses"], 125)
    def test_missing_schema_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(generate_synthetic_survey(50).drop(columns=["satisfaction"]))

if __name__ == "__main__": unittest.main()
