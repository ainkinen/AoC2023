import os

from aoc2023.day10 import find_start, part1, part2
from aoc2023.utils.files import read_as_lines

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")
TEST_INPUT_3_PATH = os.path.join(os.path.dirname(__file__), "test_input_3.txt")
TEST_INPUT_4_PATH = os.path.join(os.path.dirname(__file__), "test_input_4.txt")
TEST_INPUT_5_PATH = os.path.join(os.path.dirname(__file__), "test_input_5.txt")

grid1 = read_as_lines(TEST_INPUT_PATH)
grid2 = read_as_lines(TEST_INPUT_2_PATH)


def test_find_start():
    assert find_start(grid1) == (1, 1)
    assert find_start(grid2) == (2, 0)


def test_part1():
    assert part1(TEST_INPUT_PATH) == 4
    assert part1(TEST_INPUT_2_PATH) == 8


def test_part2():
    assert part2(TEST_INPUT_3_PATH) == 4
    assert part2(TEST_INPUT_4_PATH) == 8
    assert part2(TEST_INPUT_5_PATH) == 10
