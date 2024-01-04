import os

from aoc2023.day23 import parse_grid, part1, part2, valid_neighbours
from aoc2023.utils.files import read_as_lines

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")

grid = parse_grid(read_as_lines(TEST_INPUT_PATH))


def test_valid_neighbours():
    assert valid_neighbours((0, 1), grid, True) == {(1, 1)}
    assert valid_neighbours((3, 11), grid, True) == {(3, 10), (4, 11), (3, 12)}


def test_part1():
    assert part1(TEST_INPUT_PATH) == 94


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 154
