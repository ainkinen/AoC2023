import os
import re
from dataclasses import dataclass
from typing import Any

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass(frozen=True)
class Coord:
    y: int
    x: int


def adjacent(point: Coord) -> set[Coord]:
    return {
        Coord(y=point.y - 1, x=point.x - 1),
        Coord(y=point.y - 1, x=point.x),
        Coord(y=point.y - 1, x=point.x + 1),
        Coord(y=point.y, x=point.x - 1),
        # Coord(y=point.y, x=point.x), self
        Coord(y=point.y, x=point.x + 1),
        Coord(y=point.y + 1, x=point.x - 1),
        Coord(y=point.y + 1, x=point.x),
        Coord(y=point.y + 1, x=point.x + 1),
    }


def find_symbols(lines: list[str]) -> set[Coord]:
    coords = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if not char.isdigit() and char != ".":
                coords.add(Coord(y, x))

    return coords


def find_gear_symbols(lines: list[str]) -> set[Coord]:
    coords = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "*":
                coords.add(Coord(y, x))

    return coords


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    symbols = find_symbols(lines)

    next_to_symbols = set().union(*(adjacent(c) for c in symbols))

    part_numbers: list[int] = []

    for y, line in enumerate(lines):
        number_matches = re.finditer(r"\d+", line)

        for number_match in number_matches:
            digit_locations = [
                Coord(y=y, x=x)
                for x in range(number_match.span()[0], number_match.span()[1])
            ]

            if any((digit in next_to_symbols) for digit in digit_locations):
                part_numbers.append(int(number_match.group()))

    return sum(part_numbers)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    possible_gear_locations = find_gear_symbols(lines)

    gears: list[list[int]] = []

    # Stupid looping. Should go through the numbers once and link them to possible gear locations.
    for loc in possible_gear_locations:
        next_to_loc = adjacent(loc)

        gear_parts: list[int] = []

        for y, line in enumerate(lines):
            number_matches = re.finditer(r"\d+", line)

            for number_match in number_matches:
                digit_locations = [
                    Coord(y=y, x=x)
                    for x in range(number_match.span()[0], number_match.span()[1])
                ]

                if any((digit in next_to_loc) for digit in digit_locations):
                    gear_parts.append(int(number_match.group()))

        if len(gear_parts) == 2:
            gears.append(gear_parts)

    return sum(gear[0] * gear[1] for gear in gears)
