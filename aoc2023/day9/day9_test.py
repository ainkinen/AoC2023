import os

from aoc2023.day9 import extrapolate_next, extrapolate_previous, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


async def test_extrapolate_next():
    assert extrapolate_next([0, 3, 6, 9, 12, 15]) == 18
    assert extrapolate_next([1, 3, 6, 10, 15, 21]) == 28
    assert extrapolate_next([10, 13, 16, 21, 30, 45]) == 68


async def test_extrapolate_previous():
    assert extrapolate_previous([0, 3, 6, 9, 12, 15]) == -3
    assert extrapolate_previous([1, 3, 6, 10, 15, 21]) == 0
    assert extrapolate_previous([10, 13, 16, 21, 30, 45]) == 5


def test_part1():
    assert part1(TEST_INPUT_PATH) == 114


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 2
