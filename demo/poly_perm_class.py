import itertools

from combcov import CombCov, Rule
from permuta import Av, Perm
from tilings import Obstruction, Requirement, Tiling



class CombCovTiling(Rule):
    def __init__(self, tiling):
        self.tiling = tiling

    def get_elmnts(self, of_size):
        if of_size == 0:
            return []
        return [gp.patt for gp in self.tiling.gridded_perms_of_length(of_size)]

    def get_subrules(self):
        maxlen = 4
        if self.tiling.dimensions != (1, 1) or self.tiling.requirements:
            raise NotImplementedError("Only handle 1x1 tilings without requirements :(")

        def blocks(cell):
            incr = Obstruction.single_cell(Perm((1, 0)), cell)
            decr = Obstruction.single_cell(Perm((0, 1)), cell)
            point = [Requirement.single_cell(Perm((0,)), cell)]
            return [([incr], [point]), ([decr], [point]), ([incr, decr], [point])]

        basis = [ob.patt for ob in self.tiling.obstructions]
        res = []
        for i in range(1, maxlen + 1):
            for perm in Av(basis).of_length(i):
                cells = [(i, v) for i, v in enumerate(perm)]
                for assignment in itertools.product(*[blocks(cell) for cell in cells]):
                    obstructions = []
                    requirements = []
                    for obs, reqs in assignment:
                        obstructions.extend(obs)
                        requirements.extend(reqs)
                    res.append(CombCovTiling(Tiling(obstructions, requirements)))
        print("Number of rules is {}.".format(len(res)))
        return res

    def __hash__(self):
        return hash(self.tiling)

    def __str__(self):
        return "\n" + str(self.tiling)


def main():
    tiling = Tiling.from_string("120_012")
    cctiling = CombCovTiling(tiling)

    max_elmnt_size = 7

    print("Trying to find a cover for \n{}\n using elements up to size {}.".format(
        cctiling, max_elmnt_size))
    comb_cov = CombCov(cctiling, max_elmnt_size)
    comb_cov.solve()

    print("(Enumeration: {})".format(comb_cov.enumeration))

    for nr, solution in enumerate(comb_cov.get_solutions(), start=1):
        print("Solution nr. {}:".format(nr))
        for rule in solution:
            print(" - {}".format(rule))


if __name__ == "__main__":
    main()
