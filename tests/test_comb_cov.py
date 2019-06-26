import unittest
from unittest.mock import patch

from combcov import CombCov, ExactCover
from demo.string_set import StringSet


class CombCovTest(unittest.TestCase):
    def test_with_string_sets(self):
        alphabet = ('a', 'b')
        avoid = frozenset(['aa'])
        string_set = StringSet(alphabet, avoid)
        max_elmnt_size = 7

        solution_indices = [[0, 1, 3], ]
        with patch.object(ExactCover, 'exact_cover',
                          return_value=solution_indices):
            comb_cov = CombCov(string_set, max_elmnt_size)
            comb_cov.solve()

            solutions = comb_cov.get_solutions()
            self.assertEqual(len(solution_indices), len(solutions))

            for i, solution in enumerate(solutions):
                self.assertEqual(len(solution_indices[i]), len(solution))


class RuleTest(unittest.TestCase):
    alphabet = ('a', 'b')
    avoid = frozenset(['aa', 'bb'])
    avoid_subset = frozenset(['bb'])
    prefix = "ab"

    def setUp(self):
        self.string_set = StringSet(self.alphabet, self.avoid, self.prefix)
        self.sub_string_set = StringSet(self.alphabet, self.avoid_subset,
                                        self.prefix)

    def test_elements(self):
        max_string_length = 4
        for elmnt in self.string_set.get_elmnts(of_size=max_string_length):
            self.assertEqual(max_string_length, len(elmnt))

        elmnts = []
        for length in range(max_string_length + 1):
            elmnts.extend(self.string_set.get_elmnts(of_size=length))

        expected_rule_elmnts = frozenset(['ab', 'aba', 'abb', 'abab', 'abba'])
        self.assertEqual(expected_rule_elmnts, frozenset(elmnts))

    def test_rule_generation(self):
        rules = self.string_set.get_subrules()
        self.assertNotIn(None, rules)


if __name__ == '__main__':
    unittest.main()
