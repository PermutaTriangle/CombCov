import unittest

from permuta import Av, MeshPatt, Perm, PermSet

import pytest
from combcov import Rule
from demo.mesh_tiling import Cell, MeshTiling


class CellTest(unittest.TestCase):

    def setUp(self):
        self.mp_31c2 = MeshPatt(Perm((2, 0, 1)),
                                ((2, 0), (2, 1), (2, 2), (2, 3)))
        self.mp_cell = Cell(frozenset({self.mp_31c2}), frozenset())

    def uninitialized_cell(self):
        assert (not MeshTiling.empty_cell.is_uninitialized())
        assert (not MeshTiling.point_cell.is_uninitialized())
        assert (not MeshTiling.anything_cell.is_uninitialized())

    def test_empty_cell(self):
        assert (MeshTiling.empty_cell.is_empty())
        assert (not MeshTiling.point_cell.is_empty())
        assert (not MeshTiling.anything_cell.is_empty())

    def test_point_cell(self):
        assert (not MeshTiling.empty_cell.is_point())
        assert (MeshTiling.point_cell.is_point())
        assert (not MeshTiling.anything_cell.is_point())

    def test_anything_cell(self):
        assert (not MeshTiling.empty_cell.is_anything())
        assert (not MeshTiling.point_cell.is_anything())
        assert (MeshTiling.anything_cell.is_anything())

    def test_repr(self):
        assert repr(MeshTiling.empty_cell) == " "
        assert repr(MeshTiling.point_cell) == "o"
        assert repr(MeshTiling.anything_cell) == "S"
        assert repr(self.mp_cell) == "Av({})".format(repr(self.mp_31c2))

    def test_get_permclass(self):
        for size in range(1, 5):
            expected_from_empty_cell = set()
            assert set(MeshTiling.empty_cell.get_permclass().of_length(
                size)) == expected_from_empty_cell

            expected_from_point_cell = {Perm((0,))} if size == 1 else set()
            assert set(MeshTiling.point_cell.get_permclass().of_length(
                size)) == expected_from_point_cell

            expected_from_anything_cell = set(PermSet(size))
            assert set(MeshTiling.anything_cell.get_permclass().of_length(
                size)) == expected_from_anything_cell

            expected_from_mp_cell = set(filter(
                lambda perm: perm.avoids(self.mp_31c2),
                PermSet(size))
            )
            assert set(self.mp_cell.get_permclass().of_length(
                size)) == set(expected_from_mp_cell)
            assert (len(set(expected_from_mp_cell)) ==
                    len(list(expected_from_mp_cell)))


class PermTest(unittest.TestCase):

    def setUp(self) -> None:
        self.p = Perm((1, 0))
        self.mt = MeshTiling({(0, 0): Cell(
            obstructions=frozenset({self.p}),
            requirements=frozenset()
        )})

    def test_that_obstructions_are_perms(self) -> None:
        for subrule in self.mt.get_subrules():
            assert isinstance(subrule, Rule)
            for obstructions in subrule.get_obstruction_lists():
                for obstruction in obstructions:
                    assert isinstance(obstruction, Perm)


class MeshTilingTest(unittest.TestCase):

    def setUp(self):
        self.p_312 = Perm((2, 0, 1))
        self.mp_31c2 = MeshPatt(self.p_312, ((2, 0), (2, 1), (2, 2), (2, 3)))
        self.mp_1c2 = self.mp_31c2.sub_mesh_pattern([1, 2])

        self.root_mp_cell = Cell(frozenset({self.mp_31c2}), frozenset())
        self.sub_mp_cell = Cell(frozenset({self.mp_1c2}), frozenset())

        self.empty_mt = MeshTiling()
        self.any_mt = MeshTiling({(0, 0): MeshTiling.anything_cell})
        self.root_mt = MeshTiling({
            (0, 0): self.root_mp_cell,
        })
        self.sub_mt = MeshTiling({
            (0, 0): self.root_mp_cell,
            (1, 1): MeshTiling.point_cell,
            (2, 0): self.sub_mp_cell,
        })

    def test_is_instance_of_Rule(self):
        assert isinstance(self.sub_mt, Rule)
        assert isinstance(self.root_mt, Rule)
        assert isinstance(self.empty_mt, Rule)

    def test_padding_removal(self):
        padded_sub_mt = MeshTiling({
            (1, 1): self.root_mp_cell,
            (2, 2): MeshTiling.point_cell,
            (3, 1): self.sub_mp_cell,
        })
        assert padded_sub_mt == self.sub_mt

    def test_any_mt(self):
        any_tiling = self.any_mt.get_tiling()
        assert len(any_tiling) == 1
        assert any_tiling[0] == MeshTiling.anything_cell

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
            Cell(frozenset({self.mp_31c2}), frozenset()),
            MeshTiling.empty_cell,
            Cell(frozenset({self.mp_1c2}), frozenset()),
            MeshTiling.empty_cell,
            MeshTiling.point_cell,
            MeshTiling.empty_cell
        ]
        assert tiling == correct_tiling

    def test_get_elmnts_of_size_Av21_cell(self):
        mt = MeshTiling({
            (0, 0): Cell(
                obstructions=frozenset({Perm((1, 0))}),
                requirements=frozenset()
            ),
            (1, 1): Cell(
                obstructions=frozenset({Perm((0, 1)), Perm((1, 0))}),
                requirements=frozenset({Perm((0,))})
            )
        })

        for size in range(1, 5):
            expected_perms = set(Av([Perm((1, 0))]).of_length(size))
            mt_perms = mt.get_elmnts(of_size=size)
            assert (len(set(mt_perms)) == len(list(mt_perms)))
            assert (set(mt_perms) == expected_perms)

    def test_get_elmnts_of_size_point_cell(self):
        mt = MeshTiling({
            (0, 0): Cell(
                obstructions=frozenset({Perm((0, 1)), Perm((1, 0))}),
                requirements=frozenset({Perm((0,))})
            )
        })

        for size in range(1, 5):
            expected_perms = {Perm((0,))} if size == 1 else set()
            mt_perms = mt.get_elmnts(of_size=size)
            assert (len(set(mt_perms)) == len(list(mt_perms)))
            assert (set(mt_perms) == expected_perms)

    def test_subrules(self):
        self.root_mt.MAX_COLUMN_DIMENSION = 3
        self.root_mt.MAX_ROW_DIMENSION = 2
        self.root_mt.MAX_ACTIVE_CELLS = 3
        subrules = list(self.root_mt.get_subrules())
        assert all(isinstance(rule, Rule) for rule in subrules)
        assert (self.empty_mt in subrules)
        assert (self.any_mt in subrules)
        assert (self.root_mt in subrules)
        assert (self.sub_mt in subrules)

    def test_subrules_too_small_dimensions(self):
        self.root_mt.MAX_COLUMN_DIMENSION = 2
        self.root_mt.MAX_ROW_DIMENSION = 2
        self.root_mt.MAX_ACTIVE_CELLS = 3
        subrules = list(self.root_mt.get_subrules())
        assert all(isinstance(rule, Rule) for rule in subrules)
        assert (self.empty_mt in subrules)
        assert (self.any_mt in subrules)
        assert (self.root_mt in subrules)
        assert (self.sub_mt not in subrules)

    def test_dimensions(self):
        assert (self.empty_mt.get_dimension() == (1, 1))
        assert (self.any_mt.get_dimension() == (1, 1))
        assert (self.root_mt.get_dimension() == (1, 1))
        assert (self.sub_mt.get_dimension() == (3, 2))

    def test_length(self):
        assert (len(self.empty_mt) == 1)
        assert (len(self.any_mt) == 1)
        assert (len(self.root_mt) == 1)
        assert (len(self.sub_mt) == 6)

    def test_is_hashable(self):
        self.empty_mt.__hash__()
        self.any_mt.__hash__()
        self.root_mt.__hash__()
        self.sub_mt.__hash__()

    def test_str(self):
        assert str(self.empty_mt) == "\n --- \n|   |\n --- \n"
        assert "| Av({}) |".format(repr(self.mp_31c2)) \
               in str(self.root_mt).split("\n")


if __name__ == '__main__':
    unittest.main()
