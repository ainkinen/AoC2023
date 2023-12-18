import os

from aoc2023.day18 import part1, part2, shoelace_area

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_shoelace_area():
    assert shoelace_area([(5, 0), (6, 4), (4, 5), (1, 5), (1, 0)]) == 22


def test_part1():
    assert part1(TEST_INPUT_PATH) == 62


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 952408144115
