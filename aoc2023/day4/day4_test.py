import os

from aoc2023.day4 import Card, parse_card, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


async def test_parse_card():
    assert parse_card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == Card(
        id=1,
        lucky_numbers={41, 48, 83, 86, 17},
        numbers={83, 86, 6, 31, 17, 9, 48, 53},
    )

    assert parse_card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36") == Card(
        id=5,
        lucky_numbers={87, 83, 26, 28, 32},
        numbers={88, 30, 70, 12, 93, 22, 82, 36},
    )


def test_part1():
    assert part1(TEST_INPUT_PATH) == 13


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 30
