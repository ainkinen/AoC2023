import os

import pytest

from aoc2023.day8 import part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")
TEST_INPUT_3_PATH = os.path.join(os.path.dirname(__file__), "test_input_3.txt")


@pytest.mark.parametrize(
    "path,expected", [[TEST_INPUT_PATH, 2], [TEST_INPUT_2_PATH, 6]]
)
def test_part1(path: str, expected: int):
    assert part1(path) == expected


def test_part2():
    assert part2(TEST_INPUT_3_PATH) == 6
