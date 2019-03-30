import unittest
from unittest.mock import patch

from comb_cov import CombCov
from string_set import StringSet


class CombCovTest(unittest.TestCase):
    def test_with_string_sets(self):
        alphabet = ['a', 'b']
        avoid = ['aa']
        string_set = StringSet(alphabet, avoid)
        max_elmnt_size = 7

        with patch.object(CombCov, '_find_cover', return_value=None):
            with patch.object(CombCov, 'get_solutions_indices', return_value=[[0, 1, 3], ]):
                comb_cov = CombCov(string_set, max_elmnt_size)
                solutions_indices = comb_cov.get_solutions_indices()

                actual_solution_indices = [0, 1, 3]
                self.assertEqual(len(solutions_indices), 1)
                self.assertEqual(solutions_indices[0], actual_solution_indices)


if __name__ == '__main__':
    unittest.main()
