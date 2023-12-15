import os
from collections import defaultdict

import pytest

from aoc2023.day15 import hash_map, hash_str, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


@pytest.mark.parametrize(
    "in_str,expected",
    [
        ["HASH", 52],
        ["rn=1", 30],
        ["cm-", 253],
        ["qp=3", 97],
        ["cm=2", 47],
        ["qp-", 14],
        ["pc=4", 180],
        ["ot=9", 9],
        ["ab=5", 197],
        ["pc-", 48],
        ["pc=6", 214],
        ["ot=7", 231],
    ],
)
def test_hash_str(in_str: str, expected: int):
    assert hash_str(in_str) == expected


def test_hash_map():
    m = defaultdict(dict)

    hash_map("rn=1", m)
    assert m == {
        0: {"rn": 1},
    }

    hash_map("cm-", m)
    assert m == {
        0: {"rn": 1},
    }

    hash_map("qp=3", m)
    assert m == {
        0: {"rn": 1},
        1: {"qp": 3},
    }

    hash_map("cm=2", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        1: {"qp": 3},
    }

    hash_map("qp-", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
    }

    hash_map("pc=4", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"pc": 4},
    }

    hash_map("ot=9", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"pc": 4, "ot": 9},
    }

    hash_map("ab=5", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"pc": 4, "ot": 9, "ab": 5},
    }

    hash_map("pc-", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"ot": 9, "ab": 5},
    }

    hash_map("pc=6", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"ot": 9, "ab": 5, "pc": 6},
    }

    hash_map("ot=7", m)
    assert m == {
        0: {"rn": 1, "cm": 2},
        3: {"ot": 7, "ab": 5, "pc": 6},
    }


def test_part1():
    assert part1(TEST_INPUT_PATH) == 1320


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 145
