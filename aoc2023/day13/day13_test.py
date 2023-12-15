import os

from aoc2023.day13 import h_reflections, part1, part2, v_reflections

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_horizontal_reflection():
    assert list(
        h_reflections(
            [
                "#...##..#",
                "#....#..#",
                "..##..###",
                "#####.##.",
                "#####.##.",
                "..##..###",
                "#....#..#",
            ]
        )
    ) == [4]


def test_vertical_reflection():
    assert list(
        v_reflections(
            [
                "#.##..##.",
                "..#.##.#.",
                "##......#",
                "##......#",
                "..#.##.#.",
                "..##..##.",
                "#.#.##.#.",
            ]
        )
    ) == [5]


def test_part1():
    assert part1(TEST_INPUT_PATH) == 405


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 400
