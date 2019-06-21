import unittest

import pytest
from demo import MeshTiling
from demo.mesh_tiling import MockAvMeshPatt
from permuta import Av, MeshPatt, Perm


class MeshTilingTest(unittest.TestCase):

    def setUp(self):
        self.p_312 = Perm((2, 0, 1))
        self.mp_31c2 = MeshPatt(self.p_312, ((2, 0), (2, 1), (2, 2), (2, 3)))
        self.mp_1c2 = self.mp_31c2.sub_mesh_pattern([1, 2])

        self.point = Perm((0,))
        self.point_obstruction = [Perm((0, 1)), Perm((1, 0))]
        self.empty_cell = [[self.point], []]
        self.point_cell = [[Perm((0, 1)), Perm((1, 0))], [self.point]]

        self.empty_mt = MeshTiling({}, {})

        self.requirements = {}
        self.obstructions = {
            (0, 0): [self.mp_31c2],
        }
        self.root_mt = MeshTiling(self.requirements, self.obstructions)

        self.sub_requirements = {
            (1, 1): [self.point],
        }
        self.sub_obstructions = {
            (0, 0): [self.mp_31c2],
            (1, 1): self.point_obstruction,
            (2, 0): [self.mp_1c2],
        }
        self.sub_mt = MeshTiling(self.sub_requirements, self.sub_obstructions)

    def test_requirements_and_obstructions(self):
        assert (self.root_mt.requirements == self.requirements)
        assert (self.root_mt.obstructions == self.obstructions)
        assert (self.sub_mt.requirements == self.sub_requirements)
        assert (self.sub_mt.obstructions == self.sub_obstructions)

    def test_rows_and_columns(self):
        assert (self.empty_mt.columns == 1)
        assert (self.empty_mt.rows == 1)
        assert (self.root_mt.columns == 1)
        assert (self.root_mt.rows == 1)
        assert (self.sub_mt.columns == 3)
        assert (self.sub_mt.rows == 2)

    def test_all_avoiding_perms(self):
        mamp = MockAvMeshPatt(self.mp_1c2)
        for length, perms in [(1, [Perm((0,))]), (2, [Perm((1, 0))]),
                              (3, [Perm((2, 1, 0))])]:
            assert (set(mamp.of_length(length)) == set(perms))

    def test_number_to_coordinates_conversions(self):
        assert self.sub_mt.convert_linear_number_to_coordinates(0) == (0, 0)
        assert self.sub_mt.convert_linear_number_to_coordinates(1) == (1, 0)
        assert self.sub_mt.convert_linear_number_to_coordinates(2) == (2, 0)
        assert self.sub_mt.convert_linear_number_to_coordinates(3) == (0, 1)
        assert self.sub_mt.convert_linear_number_to_coordinates(4) == (1, 1)
        assert self.sub_mt.convert_linear_number_to_coordinates(5) == (2, 1)

        for number in (-1, 6):
            with pytest.raises(IndexError):
                self.sub_mt.convert_linear_number_to_coordinates(number)

    def test_coordinates_to_number_conversions(self):
        assert self.sub_mt.convert_coordinates_to_linear_number(0, 0) == 0
        assert self.sub_mt.convert_coordinates_to_linear_number(1, 0) == 1
        assert self.sub_mt.convert_coordinates_to_linear_number(2, 0) == 2
        assert self.sub_mt.convert_coordinates_to_linear_number(0, 1) == 3
        assert self.sub_mt.convert_coordinates_to_linear_number(1, 1) == 4
        assert self.sub_mt.convert_coordinates_to_linear_number(2, 1) == 5

        for (col, row) in [(-1, 0), (0, -1), (3, 0), (0, 2)]:
            with pytest.raises(IndexError):
                self.sub_mt.convert_coordinates_to_linear_number(col, row)

    def test_make_tiling(self):
        tiling = self.sub_mt.make_tiling()
        correct_tiling = [
            [[self.mp_31c2], []],
            self.empty_cell,
            [[self.mp_1c2], []],
            self.empty_cell,
            self.point_cell,
            self.empty_cell
        ]
        assert tiling == correct_tiling

    def test_get_elmnts_of_size_mp_31c2(self):
        mamp = MockAvMeshPatt(self.mp_31c2)
        for size in range(0, 5):
            expected_perms = set(mamp.of_length(size)) if size > 0 else set()
            mt_perms = set(self.sub_mt.get_elmnts(of_size=size))
            assert (mt_perms == expected_perms)

    def test_get_elmnts_of_size_increasing(self):
        requirements = {(1, 1): [self.point]}
        obstructions = {
            (0, 0): [Perm((1, 0))],
            (1, 1): self.point_obstruction
        }
        mt = MeshTiling(requirements, obstructions)
        for size in range(1, 5):
            expected_perms = set(Av([Perm((1, 0))]).of_length(size))
            mt_perms = set(mt.get_elmnts(of_size=size))
            assert (mt_perms == expected_perms)

    def test_get_elmnts_of_size_point(self):
        requirements = {(0, 0): [self.point]}
        obstructions = {(0, 0): self.point_obstruction}
        mt = MeshTiling(requirements, obstructions)
        for size in range(1, 5):
            expected_perms = {Perm((0,))} if size == 1 else set()
            mt_perms = set(mt.get_elmnts(of_size=size))
            assert (mt_perms == expected_perms)

    def test_get_elmnts_of_size_two_points(self):
        requirements = {
            (0, 0): [self.point],
            (1, 1): [self.point]
        }
        obstructions = {
            (0, 0): self.point_obstruction,
            (1, 1): self.point_obstruction
        }
        mt = MeshTiling(requirements, obstructions)
        for size in range(1, 5):
            expected_perms = {Perm((0, 1))} if size == 2 else set()
            mt_perms = set(mt.get_elmnts(of_size=size))
            assert (mt_perms == expected_perms)

    def test_permclass_from_cell(self):
        for size in range(1, 5):
            expected_from_empty_cell = set()
            assert set(
                self.root_mt.permclass_from_cell(self.empty_cell).of_length(
                    size)) == expected_from_empty_cell

            expected_from_point_cell = {Perm((0,))} if size == 1 else set()
            assert set(
                self.root_mt.permclass_from_cell(self.point_cell).of_length(
                    size)) == expected_from_point_cell

            mp_cell = [[self.mp_31c2], []]
            mamp = MockAvMeshPatt(mp_cell[0])
            expected_from_mp_cell = set(mamp.of_length(size))
            assert set(self.root_mt.permclass_from_cell(mp_cell).of_length(
                size)) == expected_from_mp_cell

    def test_is_point(self):
        assert self.root_mt.is_point(self.point_cell)
        assert self.root_mt.is_point(
            [[Perm((0, 1)), Perm((1, 0))], [Perm((0,))]])

    def test_is_not_point(self):
        assert not self.root_mt.is_point(self.empty_cell)
        assert not self.root_mt.is_point(
            [[Perm((0, 1)), Perm((1, 0))], Perm((0,))])

    def test_subrules(self):
        subrules = self.root_mt.get_subrules()
        assert (self.sub_mt in subrules)
        assert (self.empty_mt in subrules)


if __name__ == '__main__':
    unittest.main()
