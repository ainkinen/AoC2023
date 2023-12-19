import os

from aoc2023.day19 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_part1():
    assert part1(TEST_INPUT_PATH) == 19114


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 167409079868000
