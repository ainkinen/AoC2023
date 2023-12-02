import os

from aoc2023.day2 import part1, part2, parse_reveal, Counts, parse_game, Game, parse_id

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), 'test_input.txt')
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), 'test_input_2.txt')


def test_parse_reveal():
    assert parse_reveal('3 blue, 4 red') == Counts(blue=3, red=4)
    assert parse_reveal('1 red, 2 green, 6 blue') == Counts(red=1, green=2, blue=6)
    assert parse_reveal('2 green') == Counts(green=2)


def test_parse_id():
    assert parse_id('Game 1') == 1
    assert parse_id('Game 123') == 123


def test_parse_game():
    assert parse_game('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green') == Game(
        id=1,
        reveals=[
            Counts(blue=3, red=4),
            Counts(red=1, green=2, blue=6),
            Counts(green=2),
        ]
    )


def test_part1():
    assert part1(TEST_INPUT_PATH) == 8


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 2286
