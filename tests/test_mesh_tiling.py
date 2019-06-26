import unittest

import pytest
from combcov import Rule
from demo.mesh_tiling import Cell, MeshTiling, MockAvMeshPatt
from permuta import Av, MeshPatt, Perm, PermSet


class MockAvMeshPattTests(unittest.TestCase):

    def test_mock_av_patt_nonsense(self):
        with pytest.raises(ValueError):
            MockAvMeshPatt([None])

    def test_all_avoiding_perms(self):
        mp_1c2 = MeshPatt(Perm((0, 1)), ((1, 0), (1, 1), (1, 2)))
        mamp = MockAvMeshPatt(mp_1c2)
        for length, perms in [(1, [Perm((0,))]), (2, [Perm((1, 0))]),
                              (3, [Perm((2, 1, 0))])]:
            assert (set(mamp.of_length(length)) == set(perms))


class CellTest(unittest.TestCase):

    def setUp(self):
        self.mp_31c2 = MeshPatt(Perm((2, 0, 1)),
                                ((2, 0), (2, 1), (2, 2), (2, 3)))
        self.uninitialized_cell = Cell(None, None)
        self.empty_cell = Cell(frozenset({Perm((0,))}), frozenset())
        self.point_cell = Cell(frozenset({Perm((0, 1)), Perm((1, 0))}),
                               frozenset({Perm((0,))}))
        self.anything_cell = Cell(frozenset(), frozenset())

    def uninitialized_cell(self):
        assert (self.uninitialized_cell.is_uninitialized())
        assert (not self.empty_cell.is_uninitialized())
        assert (not self.point_cell.is_uninitialized())
        assert (not self.anything_cell.is_uninitialized())

    def test_empty_cell(self):
        assert (not self.uninitialized_cell.is_empty())
        assert (self.empty_cell.is_empty())
        assert (not self.point_cell.is_empty())
        assert (not self.anything_cell.is_empty())

    def test_point_cell(self):
        assert (not self.uninitialized_cell.is_point())
        assert (not self.empty_cell.is_point())
        assert (self.point_cell.is_point())
        assert (not self.anything_cell.is_point())

    def test_anything_cell(self):
        assert (not self.uninitialized_cell.is_anything())
        assert (not self.empty_cell.is_anything())
        assert (not self.point_cell.is_anything())
        assert (self.anything_cell.is_anything())

    def test_get_permclass(self):
        for size in range(1, 5):
            expected_from_empty_cell = set()
            assert set(self.empty_cell.get_permclass().of_length(
                size)) == expected_from_empty_cell

            expected_from_point_cell = {Perm((0,))} if size == 1 else set()
            assert set(self.point_cell.get_permclass().of_length(
                size)) == expected_from_point_cell

            expected_from_anything_cell = set(PermSet(size))
            assert set(self.anything_cell.get_permclass().of_length(
                size)) == expected_from_anything_cell

            mp_cell = Cell({self.mp_31c2}, {})
            expected_from_mp_cell = set(filter(
                lambda perm: perm.avoids(self.mp_31c2),
                PermSet(size))
            )
            assert set(mp_cell.get_permclass().of_length(
                size)) == set(expected_from_mp_cell)
            assert (len(set(expected_from_mp_cell)) ==
                    len(list(expected_from_mp_cell)))


class MeshTilingTest(unittest.TestCase):

    def setUp(self):
        self.p_312 = Perm((2, 0, 1))
        self.mp_31c2 = MeshPatt(self.p_312, ((2, 0), (2, 1), (2, 2), (2, 3)))
        self.mp_1c2 = self.mp_31c2.sub_mesh_pattern([1, 2])

        self.point = Perm((0,))
        self.point_obstruction = {Perm((0, 1)), Perm((1, 0))}

        self.uninitialized_cell = Cell(None, None)
        self.empty_cell = Cell(frozenset({Perm((0,))}), frozenset())
        self.point_cell = Cell(frozenset({Perm((0, 1)), Perm((1, 0))}),
                               frozenset({Perm((0,))}))
        self.anything_cell = Cell(frozenset(), frozenset())

        self.empty_mt = MeshTiling({}, {})
        self.root_mt = MeshTiling(
            obstructions={
                (0, 0): {self.mp_31c2}
            },
            requirements={}
        )
        self.sub_mt = MeshTiling(
            obstructions={
                (0, 0): {self.mp_31c2},
                (1, 1): self.point_obstruction,
                (2, 0): {self.mp_1c2},
            },
            requirements={
                (1, 1): {self.point},
            }
        )

    def test_is_instance_of_Rule(self):
        assert isinstance(self.sub_mt, Rule)
        assert isinstance(self.root_mt, Rule)
        assert isinstance(self.empty_mt, Rule)

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
        tiling = self.sub_mt.get_tiling()
        correct_tiling = [
            Cell({self.mp_31c2}, {}),
            self.empty_cell,
            Cell({self.mp_1c2}, {}),
            self.empty_cell,
            self.point_cell,
            self.empty_cell
        ]
        assert tiling == correct_tiling

    def test_get_elmnts_of_size_Av21_cell(self):
        requirements = {(1, 1): {self.point}}
        obstructions = {
            (0, 0): {Perm((1, 0))},
            (1, 1): self.point_obstruction
        }
        mt = MeshTiling(obstructions, requirements)
        for size in range(1, 5):
            expected_perms = set(Av([Perm((1, 0))]).of_length(size))
            mt_perms = mt.get_elmnts(of_size=size)
            assert (len(set(mt_perms)) == len(list(mt_perms)))
            assert (set(mt_perms) == expected_perms)

    def test_get_elmnts_of_size_point_cell(self):
        requirements = {(0, 0): {self.point}}
        obstructions = {(0, 0): self.point_obstruction}
        mt = MeshTiling(obstructions, requirements)
        for size in range(1, 5):
            expected_perms = {Perm((0,))} if size == 1 else set()
            mt_perms = mt.get_elmnts(of_size=size)
            assert (len(set(mt_perms)) == len(list(mt_perms)))
            assert (set(mt_perms) == expected_perms)

    def test_subrules(self):
        self.root_mt.MAX_COLUMN_DIMENSION = 3
        self.root_mt.MAX_ROW_DIMENSION = 2
        self.root_mt.MAX_ACTIVE_CELLS = 3
        subrules = self.root_mt.get_subrules()
        assert all(isinstance(rule, Rule) for rule in subrules)
        assert (self.empty_mt in subrules)
        assert (self.sub_mt in subrules)

    def test_subrules_too_small_dimensions(self):
        self.root_mt.MAX_COLUMN_DIMENSION = 2
        self.root_mt.MAX_ROW_DIMENSION = 2
        self.root_mt.MAX_ACTIVE_CELLS = 3
        subrules = self.root_mt.get_subrules()
        assert all(isinstance(rule, Rule) for rule in subrules)
        assert (self.empty_mt in subrules)
        assert (self.sub_mt not in subrules)

    def test_dimensions(self):
        assert (self.sub_mt.get_dimension() == (3, 2))
        assert (self.root_mt.get_dimension() == (1, 1))
        assert (self.empty_mt.get_dimension() == (1, 1))

    def test_length(self):
        assert (len(self.sub_mt) == 6)
        assert (len(self.root_mt) == 1)
        assert (len(self.empty_mt) == 1)

    def test_is_hashable(self):
        self.sub_mt.__hash__()
        self.root_mt.__hash__()
        self.empty_mt.__hash__()

if __name__ == '__main__':
    unittest.main()
