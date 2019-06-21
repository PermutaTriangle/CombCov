import itertools
from operator import itemgetter

from combcov import CombCov, Rule
from permuta import Av, MeshPatt, Perm, PermSet
from permuta.misc import flatten, ordered_set_partitions


class MockAvMeshPatt():
    def __init__(self, mesh_patterns):
        self.mesh_patterns = mesh_patterns
        if isinstance(mesh_patterns, MeshPatt):
            self.filter_function = lambda perm: perm.avoids(mesh_patterns)
        elif all(isinstance(mp, MeshPatt) for mp in mesh_patterns):
            self.filter_function = lambda perm: all(
                perm.avoids(mp) for mp in mesh_patterns)
        elif all(isinstance(p, Perm) for p in mesh_patterns):
            print("[WARNING] mesh_patterns are all instances of "
                  "'Perm': {}".format(mesh_patterns))
            self.filter_function = lambda perm: perm in Av(mesh_patterns)
        else:
            raise ValueError("'mesh_patterns' variable not as expected: "
                             "'{}'".format(mesh_patterns))

    def of_length(self, size):
        perm_set = PermSet(size)
        return filter(self.filter_function, perm_set)


class MeshTiling(Rule):

    # ToDo: switch argument order (as it's done in Tilings)
    def __init__(self, requirements, obstructions):
        # Constants (ToDo: make into 'cls' variables?)
        self.point = Perm((0,))
        self.point_obstruction = [Perm((0, 1)), Perm((1, 0))]
        self.uninitialized_cell = [[], []]
        self.empty_cell = [[self.point], []]
        self.point_cell = [[Perm((0, 1)), Perm((1, 0))], [self.point]]

        self.x_dim = 0
        self.y_dim = 1
        self.obs_index = 0
        self.reqs_index = 1

        def _calc_dim(reqs, obs, dimension):
            return max(
                list(reqs) + list(obs) + [(0, 0)],
                key=itemgetter(dimension)
            )[dimension]

        self.columns = _calc_dim(requirements, obstructions, self.x_dim) + 1
        self.rows = _calc_dim(requirements, obstructions, self.y_dim) + 1

        self.requirements = {k: tuple(v) for (k, v) in requirements.items()}
        self.obstructions = {k: tuple(v) for (k, v) in obstructions.items()}

        self.grid = [[[[] for _ in range(2)] for _ in range(self.rows)] for _
                     in range(self.columns)]

        # Populate requirements...
        for (c, r), req_list in requirements.items():
            self.grid[c][r][self.reqs_index] = req_list

        # ...and obstructions...
        for (c, r), obs_list in obstructions.items():
            self.grid[c][r][self.obs_index] = obs_list

        # ...and then the rest are empty cells
        for (c, r) in itertools.product(range(self.columns), range(self.rows)):
            if self.grid[c][r] == self.uninitialized_cell:
                self.grid[c][r] = self.empty_cell

    # Linear number = (column, row)
    #   -----------------------------------
    #  | 3 = (0,1) | 4 = (1,1) | 5 = (2,1) |
    #  |-----------+-----------+-----------|
    #  | 0 = (0,0) | 1 = (1,0) | 2 = (2,0) |
    #   -----------------------------------
    def convert_linear_number_to_coordinates(self, number):
        if number < 0 or number >= self.columns * self.rows:
            raise IndexError
        else:
            col = number % self.columns
            row = number // self.columns
            return (col, row)

    def convert_coordinates_to_linear_number(self, col, row):
        if col < 0 or col >= self.columns or row < 0 or row >= self.rows:
            raise IndexError
        else:
            return row * self.columns + col

    def is_point(self, cell):
        return cell[self.reqs_index] == [self.point] and cell[
            self.obs_index] == self.point_obstruction

    def make_tiling(self):
        # Flattening the 2D self.grid into a 1D list
        tiling = []
        for row in range(self.rows):
            row_content = [self.grid[i][row] for i in range(self.columns)]
            tiling.extend(row_content)
        return tiling

    def permclass_from_cell(self, cell):
        if cell == self.empty_cell:
            return Av(Perm((0,)))
        elif cell == self.point_cell:
            return PermSet(1)
        else:
            obstructions = cell[self.obs_index]
            return MockAvMeshPatt(obstructions)

    def __len__(self):
        return self.columns * self.rows

    def get_elmnts(self, of_size):
        # Return permutations of length 'of_size' on a MeshTiling like this:
        #
        #      ------------------------
        #     |          | o |         |
        #     |----------+---+---------|
        #     | Av(31#2) |   | Av(1#2) |
        #      ------------------------
        #
        # The following code was shamelessly ported and adapted from
        # PermutaTriangle/grids repo, grids/Tilings.py file

        w = self.columns
        h = self.rows

        tiling = self.make_tiling()

        def permute(arr, perm):
            res = [None] * len(arr)
            for i in range(len(arr)):
                res[i] = arr[perm[i]]
            return res

        def count_assignments(at, left):
            if at == len(self):
                # base case in recursion
                if left == 0:
                    yield []
            else:
                if self.is_point(tiling[at]):
                    # one point in cell
                    if left > 0:
                        for ass in count_assignments(at + 1, left - 1):
                            yield [1] + ass
                elif tiling[at] == self.empty_cell:
                    # no point in cell
                    for ass in count_assignments(at + 1, left):
                        yield [0] + ass
                else:
                    for cur in range(left + 1):
                        for ass in count_assignments(at + 1, left - cur):
                            yield [cur] + ass

        elmnts_list = []
        for count_ass in count_assignments(0, of_size):
            cntz = [[0 for j in range(w)] for i in range(h)]

            for i, k in enumerate(count_ass):
                (col, row) = self.convert_linear_number_to_coordinates(i)
                cntz[row][col] = k

            rowcnt = [sum(cntz[ro][co] for co in range(w)) for ro in range(h)]
            colcnt = [sum(cntz[ro][co] for ro in range(h)) for co in range(w)]

            for colpart in itertools.product(*[
                    ordered_set_partitions(
                        range(colcnt[col]), [
                            cntz[row][col] for row in range(h)
                        ]
                    ) for col in range(w)]):
                scolpart = [[sorted(colpart[i][j]) for j in range(h)] for i in
                            range(w)]
                for rowpart in itertools.product(*[
                    ordered_set_partitions(range(rowcnt[row]),
                                           [cntz[row][col] for col in
                                            range(w)]) for row in range(h)]):
                    srowpart = [[sorted(rowpart[i][j]) for j in range(w)] for i
                                in range(h)]
                    for perm_ass in itertools.product(
                            *[self.permclass_from_cell(s).of_length(cnt) for
                              cnt, s in zip(count_ass, tiling)]):
                        arr = [[[] for j in range(w)] for i in range(h)]

                        for i, perm in enumerate(perm_ass):
                            (col,
                             row) = self.convert_linear_number_to_coordinates(
                                i)
                            arr[row][col] = perm

                        res = [[None] * colcnt[col] for col in range(w)]

                        cumul = 0
                        for row in range(h):
                            for col in range(w):
                                for idx, val in zip(scolpart[col][row],
                                                    permute(srowpart[row][col],
                                                            arr[row][col])):
                                    res[col][idx] = cumul + val
                            cumul += rowcnt[row]
                        elmnts_list.append(Perm(flatten(res)))

        return elmnts_list

    def get_subrules(self):
        # Subrules are MeshTilings of sizes ranging from 1 x 1 to c x r
        # where c is the number of columns of the root object + 2 and
        # r is the number of rows in the root ojbect + 1. Each cell contains
        # a mix of requirements (Perms) and obstructions (MeshPatts) where
        # the obstructions are sub mesh patterns of any of the obstructions
        # in the root object.

        cell_choices = {self.point}
        for obstruction_list in self.obstructions.values():
            for obstruction in obstruction_list:
                if isinstance(obstruction, MeshPatt):
                    n = len(obstruction)
                    for i in range(n):
                        cell_choices.update(set(
                            obstruction.sub_mesh_pattern(indices) for indices
                            in itertools.combinations(range(n), i + 1)
                        ))
                elif isinstance(obstruction, Perm):
                    # Is there a method for sub-perms?
                    cell_choices.add(obstruction)
                else:
                    raise ValueError(
                        "[ERROR] obstruction '{}' neither MeshPatt "
                        "or Perm!".format(obstruction))

        subrules = []
        for (dim_col, dim_row) in itertools.product(range(1, self.columns + 3),
                                                    range(1, self.rows + 2)):

            nr_of_cells = dim_col * dim_row

            for how_many_active_cells in range(4):
                for active_cells in itertools.product(
                        cell_choices, repeat=how_many_active_cells):
                    for combination in itertools.combinations(
                            range(nr_of_cells), how_many_active_cells):
                        requirements = {}
                        obstructions = {}
                        for i, cell_index in enumerate(combination):
                            cell = active_cells[i]
                            col = cell_index % dim_col
                            row = cell_index // dim_col
                            if cell == self.point:
                                requirements[(col, row)] = [self.point]
                                obstructions[
                                    (col, row)] = self.point_obstruction
                            else:
                                # List of MeshPatts
                                obstructions[(col, row)] = [cell]

                        mt = MeshTiling(requirements, obstructions)
                        subrules.append(mt)

        return subrules

    def _key(self):
        return (frozenset(self.requirements.items()),
                frozenset(self.obstructions.items()))

    def __str__(self):
        return "{}".format(self.grid)


def main():
    perm = Perm((0, 2, 1))
    mesh_patt = MeshPatt(perm, ((2, 0), (2, 1), (2, 2), (2, 3)))
    requirements = {}
    obstructions = {(0, 0): mesh_patt}
    mesh_tiling = MeshTiling(requirements, obstructions)
    max_elmnt_size = 7

    print("Trying to find a cover for {} using elements up to size {}.".format(
        mesh_tiling, max_elmnt_size))
    comb_cov = CombCov(mesh_tiling, max_elmnt_size)
    comb_cov.solve()

    print("(Enumeration: {})".format(comb_cov.enumeration))

    for nr, solution in enumerate(comb_cov.get_solutions(), start=1):
        print("Solution nr. {}:".format(nr))
        for rule in solution:
            print(" - {}".format(rule))


if __name__ == "__main__":
    main()
