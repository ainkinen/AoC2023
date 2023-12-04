import os

import pytest

from aoc2023.day1 import any_digits, num_digits, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_num_digits():
    assert num_digits("1abc2") == ["1", "2"]
    assert num_digits("treb7uchet") == ["7"]

    with pytest.raises(ValueError):
        num_digits("fizzbuzz")

    with pytest.raises(ValueError):
        num_digits("onetwothree")


def test_any_digits():
    assert any_digits("abcone2threexyz") == ["1", "3"]
    assert any_digits("7pqrstsixteen") == ["7", "6"]

    assert any_digits("8one1rjtnhjx") == ["8", "1"]
    assert any_digits("eightthree3ninekzhtlqsevenssprmrqhhgncrs") == ["8", "7"]
    assert any_digits("6one8nlzxfxvr") == ["6", "8"]
    assert any_digits("4cgm9fivethree") == ["4", "3"]
    assert any_digits("four77gxvdqztzzgbsxhntwortndzqzj") == ["4", "2"]
    assert any_digits("t8three335") == ["8", "5"]
    assert any_digits("c2rjggzl") == ["2", "2"]
    assert any_digits("jjgjbqgbnz4gdsqk66991") == ["4", "1"]
    assert any_digits("ninezckbpsr9") == ["9", "9"]
    assert any_digits("jb5sevenseven") == ["5", "7"]
    assert any_digits("one5nfdcvx") == ["1", "5"]
    assert any_digits("1kbcmclhrh1onejzft") == ["1", "1"]
    assert any_digits("fiveninefivedglztnjxblonehfive3") == ["5", "3"]
    assert any_digits("6onesixh6onethree9") == ["6", "9"]
    assert any_digits("spdzhnt5tpzrkh1fxlnine4skgzdln") == ["5", "4"]
    assert any_digits("1onenineqgzcq2eightwonh") == ["1", "2"]
    assert any_digits("vfzvds826vtlrcg6rvseven") == ["8", "7"]
    assert any_digits("vqmoneight9tknqtcsmb") == ["1", "9"]
    assert any_digits("kqrcrqrqjbdeight7ckhr23") == ["8", "3"]

    with pytest.raises(ValueError):
        any_digits("zero")


def test_part1():
    assert part1(TEST_INPUT_PATH) == 142


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 281
