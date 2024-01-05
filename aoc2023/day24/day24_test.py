import os

from aoc2023.day24 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_part1():
    assert part1(TEST_INPUT_PATH, area_min=7, area_max=27) == 2


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 47
