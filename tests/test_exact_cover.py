import os
import unittest
from pathlib import Path
from subprocess import DEVNULL, Popen
from unittest.mock import patch

from combcov import ExactCover


def _mocked_call_Popen(self, inp, outp):
    dir = str(Path(__file__).parents[0])
    av_21_inp_lp = os.path.join(dir, 'av_21', 'inp.lp')
    av_21_out_sol = os.path.join(dir, 'av_21', 'out.sol')

    if [row for row in open(inp)] == [row for row in open(av_21_inp_lp)]:
        with open(av_21_out_sol, 'r') as from_file:
            with open(outp, 'w') as to_file:
                for line in from_file:
                    to_file.write(line)

        return Popen('true', shell=True, stdout=DEVNULL)
    else:
        return Popen('false', shell=True, stdout=DEVNULL)


class GurobiExactCover(unittest.TestCase):
    av_21_bitstrings = [1, 2, 4, 8, 28, 30]
    av_21_solution = [0, 5]
    cover_string_length = 5

    def test_perm_av_21_with_gurobi_mocked_out(self):
        with patch.object(ExactCover, '_call_Popen', _mocked_call_Popen):
            ec = ExactCover(self.av_21_bitstrings, self.cover_string_length)
            solution = ec.exact_cover()
            self.assertEqual(solution, self.av_21_solution)


class FailingExactCover(unittest.TestCase):
    nonsense_bitstrings = [1, 1, 2]
    nonsense_length = 112

    def test_with_failing_Popen(self):
        with patch.object(ExactCover, '_call_Popen', _mocked_call_Popen):
            ec = ExactCover(self.nonsense_bitstrings, self.nonsense_length)
            self.assertRaises(RuntimeError, ec.exact_cover)


if __name__ == '__main__':
    unittest.main()
