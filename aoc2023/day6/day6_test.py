import os

from aoc2023.day6 import get_winning_presses, part1, part2, travel_distance

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_travel_distance():
    assert travel_distance(0, 7) == 0
    assert travel_distance(1, 7) == 6
    assert travel_distance(2, 7) == 10
    assert travel_distance(3, 7) == 12
    assert travel_distance(4, 7) == 12
    assert travel_distance(5, 7) == 10
    assert travel_distance(6, 7) == 6
    assert travel_distance(7, 7) == 0


def test_get_winning_presses():
    assert get_winning_presses(7, 9) == [2, 3, 4, 5]
    assert get_winning_presses(15, 40) == [4, 5, 6, 7, 8, 9, 10, 11]
    assert get_winning_presses(30, 200) == [11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_part1():
    assert part1(TEST_INPUT_PATH) == 288


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 71503
