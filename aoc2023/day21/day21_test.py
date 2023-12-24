import os

from aoc2023.day21 import part1

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_part1():
    assert part1(TEST_INPUT_PATH, steps=6) == 16
