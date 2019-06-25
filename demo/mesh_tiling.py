import itertools
from operator import itemgetter

from combcov import CombCov, Rule
from permuta import Av, MeshPatt, Perm, PermSet
from permuta.misc import flatten, ordered_set_partitions


# ToDo: Cell blocks as done in grids repo
# Cell = namedtuple("Cell", ["x", "y"])


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

    def __init__(self, obstructions, requirements):
        # Constants (ToDo: make into 'cls' variables?)
        self.anything = Av([])
        self.point = Perm((0,))
        self.point_obstruction = [Perm((0, 1)), Perm((1, 0))]
        self.empty_cell = [[self.point], []]
        self.point_cell = [[Perm((0, 1)), Perm((1, 0))], [self.point]]
        self.uninitialized_cell = [None, None]
        self.avoiding_nothing_cell = [[], []]

        self.x_dim = 0
        self.y_dim = 1
        self.obs_index = 0
        self.reqs_index = 1

        self.MAX_COLUMN_DIMENSION = 3
        self.MAX_ROW_DIMENSION = 3
        self.MAX_ACTIVE_CELLS = 3

        def _calc_dim(reqs, obs, dimension):
            return max(
                list(reqs) + list(obs) + [(0, 0)],
                key=itemgetter(dimension)
            )[dimension]

        self.columns = _calc_dim(requirements, obstructions, self.x_dim) + 1
        self.rows = _calc_dim(requirements, obstructions, self.y_dim) + 1

        self.obstructions = {k: tuple(v) for (k, v) in obstructions.items()}
        self.requirements = {k: tuple(v) for (k, v) in requirements.items()}

        self.grid = [[[None, None] for _ in range(self.rows)] for _
                     in range(self.columns)]

        # Populate obstructions...
        for (c, r), obs_list in obstructions.items():
            self.grid[c][r][self.obs_index] = obs_list
            self.grid[c][r][self.reqs_index] = []

        # ...and requirements...
        for (c, r), req_list in requirements.items():
            self.grid[c][r][self.reqs_index] = req_list
            if self.grid[c][r][self.obs_index] is None:
                self.grid[c][r][self.obs_index] = []

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

    # Instead of row-by-row, go column-by-column when flattening?
    def make_tiling(self):
        # Flattening the 2D self.grid into a 1D list
        tiling = []
        for row in range(self.rows):
            row_content = [self.grid[i][row] for i in range(self.columns)]
            tiling.extend(row_content)
        return tiling

    # Function on the Cell object?
    def is_point(self, cell):
        return cell[self.reqs_index] == [self.point] and cell[
            self.obs_index] == self.point_obstruction

    # Function on the Cell object?
    def permclass_from_cell(self, cell):
        if cell == self.empty_cell:
            return Av(Perm((0,)))
        elif cell == self.point_cell:
            return PermSet(1)
        elif cell == self.avoiding_nothing_cell:
            return PermSet()
        else:
            obstructions = cell[self.obs_index]
            return MockAvMeshPatt(obstructions)

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
        # Subrules are MeshTilings of sizes ranging from 1 x 1 to 3 x 3
        # (adjustable with self.MAX_COLUMN_DIMENSION and self.MAX_ROW_DIMENSION
        # vairables). Each cell contains a mix of requirements (Perms) and
        # obstructions (MeshPatts) where the obstructions are sub mesh patterns
        # of any of the obstructions in the root object.

        cell_choices = {self.point, self.anything}
        for obstruction_list in self.obstructions.values():
            for obstruction in obstruction_list:
                if isinstance(obstruction, MeshPatt):
                    n = len(obstruction)
                    for i in range(n):
                        for indices in itertools.combinations(range(n), i + 1):
                            sub_mesh_pattern = obstruction.sub_mesh_pattern(
                                indices)
                            shading = sub_mesh_pattern.shading
                            if len(sub_mesh_pattern) == 1:
                                x = {c[0] for c in shading}
                                y = {c[1] for c in shading}
                                if len(shading) <= 1:
                                    pass
                                elif len(shading) == 2 and (
                                        len(x) == 1 or len(y) == 1):
                                    pass
                                else:
                                    cell_choices.add(sub_mesh_pattern)
                            else:
                                cell_choices.add(sub_mesh_pattern)
                elif isinstance(obstruction, Perm):
                    # Is there a method for sub-perms?
                    cell_choices.add(obstruction)
                else:
                    raise ValueError(
                        "[ERROR] obstruction '{}' is neither a MeshPatt "
                        "or Perm!".format(obstruction))

        subrules = []
        for (dim_col, dim_row) in itertools.product(
                    range(1, self.columns + self.MAX_COLUMN_DIMENSION),
                    range(1, self.rows + self.MAX_ROW_DIMENSION)
                ):

            nr_of_cells = dim_col * dim_row

            for how_many_active_cells in range(self.MAX_ACTIVE_CELLS + 1):
                for active_cells in itertools.product(
                        cell_choices, repeat=how_many_active_cells):
                    for combination in itertools.combinations(
                            range(nr_of_cells), how_many_active_cells):
                        requirements = {}
                        obstructions = {}
                        for i, cell_index in enumerate(combination):
                            choice = active_cells[i]
                            col = cell_index % dim_col
                            row = cell_index // dim_col
                            if choice == self.point:
                                obstructions[
                                    (col, row)] = self.point_obstruction
                                requirements[(col, row)] = [self.point]
                            elif choice == self.anything:
                                obstructions[(col, row)] = []
                                requirements[(col, row)] = []
                            else:
                                # List of MeshPatts
                                obstructions[(col, row)] = [choice]

                        mt = MeshTiling(obstructions, requirements)
                        subrules.append(mt)

        print("[INFO] Total of {} subrules".format(len(subrules)))
        return subrules

    def get_dimension(self):
        return (self.columns, self.rows)

    def _key(self):
        return (frozenset(self.requirements.items()),
                frozenset(self.obstructions.items()))

    def __len__(self):
        return self.columns * self.rows

    def __str__(self):
        return "({}x{}) {}".format(self.columns, self.rows, self.grid)


def main():
    perm = Perm((2, 0, 1))
    mesh_patt = MeshPatt(perm, ((2, 0), (2, 1), (2, 2), (2, 3)))
    mesh_tiling = MeshTiling(
        obstructions={(0, 0): [mesh_patt]},
        requirements={}
    )
    mesh_tiling.MAX_COLUMN_DIMENSION = 3
    mesh_tiling.MAX_ROW_DIMENSION = 2
    mesh_tiling.MAX_ACTIVE_CELLS = 3

    max_elmnt_size = 5
    comb_cov = CombCov(mesh_tiling, max_elmnt_size)
    comb_cov.solve()

    for nr, solution in enumerate(comb_cov.get_solutions(), start=1):
        print("Solution nr. {}:".format(nr))
        for i, rule in enumerate(solution, start=1):
            bitstring = comb_cov.rules_to_bitstring_dict[rule]
            print(" - Rule #{}: {} with bitstring {}".format(
                i, rule, bitstring))


if __name__ == "__main__":
    main()
