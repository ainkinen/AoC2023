import os
from itertools import combinations, groupby

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Grid = list[str]
Coord = tuple[int, int]  # y, x


# https://docs.python.org/3/library/itertools.html
def all_equal(iterable):
    """Returns True if all the elements are equal to each other"""
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def transpose(grid: Grid) -> Grid:
    return ["".join(z) for z in zip(*grid)]


def get_galaxy_coords(grid: Grid) -> set[Coord]:
    height = len(grid)
    width = len(grid[0])
    return set((y, x) for y in range(height) for x in range(width) if grid[y][x] == "#")


def distance(a: Coord, b: Coord) -> int:
    d_y = abs(b[0] - a[0])
    d_x = abs(b[1] - a[1])
    return d_y + d_x


def multiplied_distance(
    a: Coord,
    b: Coord,
    row_multipliers: dict[int, int],
    column_multipliers: dict[int, int],
) -> int:
    y_range = range(min(a[0], b[0]), max(a[0], b[0]))
    x_range = range(min(a[1], b[1]), max(a[1], b[1]))

    d_y = sum(row_multipliers[y] for y in y_range)
    d_x = sum(column_multipliers[x] for x in x_range)

    return d_y + d_x


def part1(input_path: str = INPUT_PATH) -> int:
    grid = read_as_lines(input_path)

    with_expanded_rows: Grid = []
    for row in grid:
        multiples = 2 if all_equal(row) else 1
        with_expanded_rows = [*with_expanded_rows, *([row] * multiples)]

    with_expanded_columns: Grid = []
    for column in transpose(with_expanded_rows):
        multiples = 2 if all_equal(column) else 1
        with_expanded_columns = [*with_expanded_columns, *([column] * multiples)]

    expanded_grid = transpose(with_expanded_columns)

    galaxies = get_galaxy_coords(expanded_grid)

    pairs = combinations(galaxies, 2)

    distances = [distance(a, b) for a, b in pairs]

    return sum(distances)


def part2(input_path: str = INPUT_PATH, multiplier=1000000) -> int:
    grid = read_as_lines(input_path)

    row_multipliers: dict[int, int] = dict()
    for y, row in enumerate(grid):
        row_multipliers[y] = multiplier if all_equal(row) else 1

    column_multipliers: dict[int, int] = dict()
    for x, column in enumerate(transpose(grid)):
        column_multipliers[x] = multiplier if all_equal(column) else 1

    galaxies = get_galaxy_coords(grid)

    pairs = combinations(galaxies, 2)

    distances = [
        multiplied_distance(a, b, row_multipliers, column_multipliers) for a, b in pairs
    ]

    return sum(distances)
