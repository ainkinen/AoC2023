import os

from aoc2023.day11 import (
    distance,
    get_galaxy_coords,
    multiplied_distance,
    part1,
    part2,
    transpose,
)
from aoc2023.utils.files import read_as_lines

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")

grid1 = read_as_lines(TEST_INPUT_PATH)


def test_transpose():
    assert transpose(["123", "456", "789"]) == ["147", "258", "369"]
    assert transpose(["abc", "def"]) == ["ad", "be", "cf"]


def test_distance():
    assert distance((6, 1), (11, 5)) == 9
    assert distance((0, 4), (10, 9)) == 15
    assert distance((2, 0), (7, 12)) == 17
    assert distance((11, 0), (11, 5)) == 5


def test_multiplied_distance():
    y_mul = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
    x_mul = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
    assert multiplied_distance((0, 0), (4, 2), y_mul, x_mul) == 10 + 9


def test_get_galaxy_coords():
    assert get_galaxy_coords(grid1) == {
        (0, 3),
        (1, 7),
        (2, 0),
        (4, 6),
        (5, 1),
        (6, 9),
        (8, 7),
        (9, 0),
        (9, 4),
    }


def test_part1():
    assert part1(TEST_INPUT_PATH) == 374


def test_part2():
    assert part2(TEST_INPUT_2_PATH, 10) == 1030
    assert part2(TEST_INPUT_2_PATH, 100) == 8410
