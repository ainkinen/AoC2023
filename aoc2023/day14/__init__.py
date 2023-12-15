import os
from typing import Iterable

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int]  # y, x


def find_symbols(lines: list[str], symbol: str) -> set[Coord]:
    symbols = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == symbol:
                symbols.append((y, x))

    return set(symbols)


def tilt_north(rocks: Iterable[Coord], cubes: Iterable[Coord]) -> set[Coord]:
    moved_rocks: set[Coord] = set()
    rocks_from_n = sorted(rocks, key=lambda c: c[0])
    for rock in rocks_from_n:
        y, x = rock
        while True:
            next_spot = y - 1, x

            if next_spot[0] < 0 or next_spot in moved_rocks or next_spot in cubes:
                break

            y, x = next_spot

        moved_rocks.add((y, x))

    return moved_rocks


def tilt_west(rocks: Iterable[Coord], cubes: Iterable[Coord]) -> set[Coord]:
    moved_rocks: set[Coord] = set()
    rocks_from_w = sorted(rocks, key=lambda c: c[1])
    for rock in rocks_from_w:
        y, x = rock
        while True:
            next_spot = y, x - 1

            if next_spot[1] < 0 or next_spot in moved_rocks or next_spot in cubes:
                break

            y, x = next_spot

        moved_rocks.add((y, x))

    return moved_rocks


def tilt_south(
    rocks: Iterable[Coord], cubes: Iterable[Coord], y_max: int
) -> set[Coord]:
    moved_rocks: set[Coord] = set()
    rocks_from_s = sorted(rocks, key=lambda c: c[0], reverse=True)
    for rock in rocks_from_s:
        y, x = rock
        while True:
            next_spot = y + 1, x

            if next_spot[0] >= y_max or next_spot in moved_rocks or next_spot in cubes:
                break

            y, x = next_spot

        moved_rocks.add((y, x))

    return moved_rocks


def tilt_east(rocks: Iterable[Coord], cubes: Iterable[Coord], x_max: int) -> set[Coord]:
    moved_rocks: set[Coord] = set()
    rocks_from_e = sorted(rocks, key=lambda c: c[1], reverse=True)
    for rock in rocks_from_e:
        y, x = rock
        while True:
            next_spot = y, x + 1

            if next_spot[1] >= x_max or next_spot in moved_rocks or next_spot in cubes:
                break

            y, x = next_spot

        moved_rocks.add((y, x))

    return moved_rocks


def print_out(rocks: set[Coord], cubes: set[Coord], max_y: int, max_x: int):
    grid = [["." for _ in range(max_x)] for _ in range(max_y)]

    for r in rocks:
        grid[r[0]][r[1]] = "O"

    for c in cubes:
        grid[c[0]][c[1]] = "#"

    lines = ["".join(row) for row in grid]
    print("\n".join(lines))


def cycle(rocks: set[Coord], cubes: set[Coord], max_y: int, max_x: int) -> set[Coord]:
    rocks = tilt_north(rocks, cubes)
    rocks = tilt_west(rocks, cubes)
    rocks = tilt_south(rocks, cubes, max_y)
    return tilt_east(rocks, cubes, max_x)


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    rocks = find_symbols(lines, "O")
    cubes = find_symbols(lines, "#")

    moved_rocks = tilt_north(rocks, cubes)

    return sum(len(lines) - r[0] for r in moved_rocks)


def part2(input_path: str = INPUT_PATH, cycles: int = 1000000000) -> int:
    lines = read_as_lines(input_path)
    rocks = find_symbols(lines, "O")
    cubes = find_symbols(lines, "#")

    history: list[set[Coord]] = []

    for i in range(cycles):
        rocks = cycle(rocks, cubes, len(lines), len(lines[0]))

        if rocks in history:
            # Loop found
            h_idx = history.index(rocks)
            loop_len = i - h_idx
            mod = (cycles - (i + 1)) % loop_len
            return sum(len(lines) - r[0] for r in history[h_idx + mod])

        history.append(rocks)

    return sum(len(lines) - r[0] for r in history[i])
