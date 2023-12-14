import os
from enum import StrEnum
from typing import assert_never

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int]  # (y, x)
Grid = list[str]


class Dir(StrEnum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


tiles: dict[str, set[Dir]] = {
    "|": {Dir.N, Dir.S},
    "-": {Dir.E, Dir.W},
    "L": {Dir.N, Dir.E},
    "J": {Dir.N, Dir.W},
    "7": {Dir.S, Dir.W},
    "F": {Dir.S, Dir.E},
}


def invert(d: Dir) -> Dir:
    match d:
        case Dir.N:
            return Dir.S
        case Dir.S:
            return Dir.N
        case Dir.E:
            return Dir.W
        case Dir.W:
            return Dir.E
        case _:
            assert_never(d)


def find_start(grid: Grid) -> Coord:
    arr = "".join(grid)
    start_idx = arr.index("S")
    return divmod(start_idx, len(grid[0]))


def get_path(start: Coord, start_dir: Dir, grid: list[str]) -> list[Coord]:
    path: list[Coord] = [start]
    cur_dir: Dir = start_dir

    while True:
        next_y, next_x = next_tile_coord(path[-1], cur_dir)
        next_tile = grid[next_y][next_x]

        entering_from = invert(cur_dir)
        next_tile_is_valid = (
            next_tile in tiles.keys() and entering_from in tiles[next_tile]
        )
        if next_tile_is_valid:
            path.append((next_y, next_x))
            t = tiles[next_tile]
            cur_dir = (t - {entering_from}).pop()
        else:
            return path


def next_tile_coord(cur_coord: Coord, d: Dir) -> Coord:
    y, x = cur_coord
    match d:
        case Dir.N:
            return y - 1, x
        case Dir.S:
            return y + 1, x
        case Dir.E:
            return y, x + 1
        case Dir.W:
            return y, x - 1
        case _:
            assert_never(d)


def part1(input_path: str = INPUT_PATH) -> int:
    grid = read_as_lines(input_path)

    start = find_start(grid)

    paths = [get_path(start, Dir(start_d), grid) for start_d in list(Dir)]
    longest_path = max(paths, key=len)

    # grid_dimension = len(grid[0])
    # path_coords = set(longest_path)
    # picture = ""
    # for y in range(grid_dimension):
    #     for x in range(grid_dimension):
    #         if (y, x) in path_coords:
    #             picture += grid[y][x]
    #         else:
    #             picture += "."
    #     picture += "\n"
    #
    # print(picture)

    return len(longest_path) // 2


def part2(input_path: str = INPUT_PATH) -> int:
    grid = read_as_lines(input_path)

    start = find_start(grid)

    paths = [get_path(start, Dir(start_d), grid) for start_d in list(Dir)]
    longest_path = max(paths, key=len)

    path_coords = set(longest_path)

    count = 0
    enclosed = False
    last_turn = None
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if (y, x) not in path_coords:
                count += int(enclosed)
                continue
            # Keep track of boundary crossing
            if char == "|":
                enclosed = not enclosed
                continue
            # Turns are a boundary if they match with a previous one
            if char == "7":
                if last_turn == "L":
                    enclosed = not enclosed
                last_turn = "7"
                continue
            if char == "L":
                last_turn = "L"
                continue
            if char == "J":
                if last_turn == "F":
                    enclosed = not enclosed
                last_turn = "J"
                continue
            if char == "F":
                last_turn = "F"
                continue

    return count
