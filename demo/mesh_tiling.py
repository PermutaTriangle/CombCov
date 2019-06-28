import itertools
from collections import namedtuple
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


class Cell(namedtuple('Cell', ['obstructions', 'requirements'])):
    __slots__ = ()

    def is_uninitialized(self):
        return self.obstructions is None and self.requirements is None

    def is_empty(self):
        return self.obstructions == frozenset({Perm((0,))})

    def is_point(self):
        return self.obstructions == frozenset({Perm((0, 1)), Perm((1, 0))}) \
               and self.requirements == frozenset({Perm((0,))})

    def is_anything(self):
        return self.obstructions == frozenset() \
               and self.requirements == frozenset()

    def get_permclass(self):
        if self.is_empty():
            return Av(Perm((0,)))
        elif self.is_point():
            return PermSet(1)
        elif self.is_anything():
            return PermSet()
        else:
            return MockAvMeshPatt(self.obstructions)

    def __repr__(self):
        if self.is_empty():
            return " "
        elif self.is_point():
            return "o"
        elif self.is_anything():
            return "S"
        else:
            return "Av({})".format(", ".join(
                repr(mp) for mp in self.obstructions))

    def __str__(self):
        # ToDo: Instead return multiline mesh patterns
        return repr(self)


class MeshTiling(Rule):

    def __init__(self, obstructions, requirements):
        # Constants (ToDo: make into 'cls' variables?)
        self.uninitialized_cell = Cell(None, None)
        self.empty_cell = Cell(frozenset({Perm((0,))}), frozenset())
        self.point_cell = Cell(frozenset({Perm((0, 1)), Perm((1, 0))}),
                               frozenset({Perm((0,))}))
        self.anything_cell = Cell(frozenset(), frozenset())

        self.MAX_COLUMN_DIMENSION = 3
        self.MAX_ROW_DIMENSION = 3
        self.MAX_ACTIVE_CELLS = 3

        def _calc_dim(reqs, obs, dimension):
            return max(
                list(reqs) + list(obs) + [(0, 0)],
                key=itemgetter(dimension)
            )[dimension]

        self.columns = _calc_dim(requirements, obstructions, 0) + 1
        self.rows = _calc_dim(requirements, obstructions, 1) + 1

        self.obstructions = {k: tuple(v) for (k, v) in obstructions.items()}
        self.requirements = {k: tuple(v) for (k, v) in requirements.items()}

        self.grid = [[self.uninitialized_cell for _ in range(self.rows)] for _
                     in range(self.columns)]

        # Populate obstructions...
        for (c, r), obs_list in obstructions.items():
            self.grid[c][r] = Cell(set(obs_list), {})

        # ...and requirements...
        for (c, r), req_list in requirements.items():
            previous_obstruction_list = self.grid[c][r].obstructions
            self.grid[c][r] = Cell(previous_obstruction_list, req_list)

        # ...and then the rest are empty cells
        for (c, r) in itertools.product(range(self.columns), range(self.rows)):
            if self.grid[c][r].is_uninitialized():
                self.grid[c][r] = self.empty_cell

        # Flattening the 2D self.grid into a 1D list
        # (Instead of row-by-row, go column-by-column when flattening?)
        self.tiling = []
        for row in range(self.rows):
            row_content = [self.grid[i][row] for i in range(self.columns)]
            self.tiling.extend(row_content)

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

        tiling = self.tiling

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
                if tiling[at].is_point():
                    # one point in cell
                    if left > 0:
                        for ass in count_assignments(at + 1, left - 1):
                            yield [1] + ass
                elif tiling[at].is_empty():
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
                            *[s.get_permclass().of_length(cnt) for
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

        cell_choices = {self.point_cell, self.anything_cell}
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
                                xs = {c[0] for c in shading}
                                ys = {c[1] for c in shading}
                                if len(shading) <= 1:
                                    pass
                                elif len(shading) == 2 and (
                                        len(xs) == 1 or len(ys) == 1):
                                    pass
                                else:
                                    cell_choices.add(
                                        Cell(frozenset({sub_mesh_pattern}),
                                             frozenset({}))
                                    )
                            else:
                                cell_choices.add(
                                    Cell(frozenset({sub_mesh_pattern}),
                                         frozenset({}))
                                )
                elif isinstance(obstruction, Perm):
                    # Is there a method for sub-perms?
                    print("[WARNING] Cell choice is an obstruction of Perms")
                    cell_choices.add(
                        Cell(frozenset({obstruction}), frozenset({}))
                    )
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
                            c = cell_index % dim_col
                            r = cell_index // dim_col

                            if choice.obstructions is not frozenset():
                                obstructions[(c, r)] = choice.obstructions

                            if choice.requirements is not frozenset():
                                requirements[(c, r)] = choice.requirements

                        mt = MeshTiling(obstructions, requirements)
                        subrules.append(mt)

        print("[INFO] Total of {} subrules".format(len(subrules)))
        return subrules

    def get_dimension(self):
        return (self.columns, self.rows)

    def get_tiling(self):
        return self.tiling

    def _key(self):
        return (frozenset(self.requirements.items()),
                frozenset(self.obstructions.items()))

    def __len__(self):
        return self.columns * self.rows

    def __str__(self):
        # ToDo: Implement proper multiline Cell.__str__() and use instead
        tiling_representation = [repr(cell) for cell in self.tiling]

        col_widths = [
            max(len(tiling_representation[
                self.convert_coordinates_to_linear_number(col, row)
            ]) for row in range(self.rows)) + 2 for col in range(self.columns)
        ]

        top_bottom_lines = " " + "-".join("-" * l for l in col_widths) + "\n"
        middle_lines = "|" + "+".join("-" * l for l in col_widths) + "|\n"

        cell_lines = ["|" + "|".join("{:^{}}".format(
            tiling_representation[
                self.convert_coordinates_to_linear_number(col, row)],
            col_widths[col]) for col in range(self.columns)
        ) + "|\n" for row in reversed(range(self.rows))]

        return "\n" + \
            top_bottom_lines + \
            middle_lines.join(line for line in cell_lines) + \
            top_bottom_lines


def main():
    perm = Perm((2, 0, 1))
    mesh_patt = MeshPatt(perm, ((2, 0), (2, 1), (2, 2), (2, 3)))
    mesh_tiling = MeshTiling(
        obstructions={(0, 0): {mesh_patt}},
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
            (cols, rows) = rule.get_dimension()
            bitstring = comb_cov.rules_to_bitstring_dict[rule]
            print("Rule #{} of dimension {}x{} with bitstring {}: "
                  "{}".format(i, cols, rows, bitstring, rule))


if __name__ == "__main__":
    main()
