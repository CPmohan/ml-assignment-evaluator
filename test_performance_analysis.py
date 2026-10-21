import unittest

from performance_analysis import cohens_kappa


class CohensKappaTest(unittest.TestCase):
    def test_computes_observed_agreement_adjusted_for_chance(self):
        self.assertAlmostEqual(cohens_kappa([0, 1, 1, 0], [0, 1, 0, 0]), 0.5)

    def test_returns_none_when_expected_agreement_is_one(self):
        self.assertIsNone(cohens_kappa([1, 1], [1, 1]))


if __name__ == "__main__":
    unittest.main()