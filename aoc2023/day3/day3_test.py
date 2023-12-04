import os

from aoc2023.day3 import Coord, adjacent, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_adjacent():
    assert adjacent(Coord(1, 1)) == {
        Coord(y=0, x=0),
        Coord(y=0, x=1),
        Coord(y=0, x=2),
        Coord(y=1, x=0),
        # Coord(y=1, x=1) self
        Coord(y=1, x=2),
        Coord(y=2, x=0),
        Coord(y=2, x=1),
        Coord(y=2, x=2),
    }


def test_part1():
    assert part1(TEST_INPUT_PATH) == 4361


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 467835
