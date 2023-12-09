import os
from functools import reduce
from typing import Any, Iterable

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def _all_are(iterable: Iterable, expected: Any):
    return all(v == expected for v in iterable)


def generate_stack(history: list[int]) -> list[list[int]]:
    stack: list[list[int]] = [history]

    # Greate all layers
    while not _all_are(stack[-1], 0):
        new_layer: list[int] = [b - a for a, b in zip(stack[-1], stack[-1][1:])]
        stack.append(new_layer)

    return stack


def extrapolate_next(history: list[int]) -> int:
    stack = generate_stack(history)
    # Reduce down the next value
    return reduce(lambda acc, layer: acc + layer[-1], reversed(stack), 0)


def extrapolate_previous(history: list[int]) -> int:
    stack = generate_stack(history)
    # Reduce down the next value
    return reduce(lambda acc, layer: layer[0] - acc, reversed(stack), 0)


def part1(input_path: str = INPUT_PATH) -> int:
    histories = [
        [int(num) for num in line.split(" ")] for line in (read_as_lines(input_path))
    ]

    next_values = [extrapolate_next(history) for history in histories]

    return sum(next_values)


def part2(input_path: str = INPUT_PATH) -> int:
    histories = [
        [int(num) for num in line.split(" ")] for line in (read_as_lines(input_path))
    ]

    previous_values = [extrapolate_previous(history) for history in histories]

    return sum(previous_values)
