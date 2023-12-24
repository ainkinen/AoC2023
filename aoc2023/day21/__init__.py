import os

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int]  # y, x
Grid = dict[Coord, str]  # coord, content


def parse_grid(lines: list[str]) -> Grid:
    return {(y, x): char for y, line in enumerate(lines) for x, char in enumerate(line)}


def find_symbol(grid: Grid, symbol: str) -> Coord:
    for coord, content in grid.items():
        if content == symbol:
            return coord

    raise Exception(f"Symbol not found {symbol}")


def next_to(coord: Coord) -> list[Coord]:
    y, x = coord
    return [(y + dy, x + dx) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))]


def mod_coord(coord: Coord, len_y: int, len_x: int) -> Coord:
    y, x = coord

    return (y % len_y), (x % len_x)


def next_locs(cur_locs: set[Coord], grid: Grid) -> set[Coord]:
    len_y = max(c[0] for c in grid.keys()) + 1
    len_x = max(c[1] for c in grid.keys()) + 1

    def valid(coord: Coord) -> bool:
        mod = mod_coord(coord, len_y, len_x)

        return grid[mod] in ".S"

    nxt: set[Coord] = set()

    for loc in cur_locs:
        nxt.update(filter(valid, next_to(loc)))

    return nxt


def spots_in_range(start: Coord, grid: Grid, max_steps: int) -> set[Coord]:
    locs: set[Coord] = {start}
    for step in range(max_steps):
        locs = next_locs(locs, grid)

    return locs


def quad(y: list[int], n: int):
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c


def part1(input_path: str = INPUT_PATH, steps: int = 64) -> int:
    grid = parse_grid(read_as_lines(input_path))
    start = find_symbol(grid, "S")

    return len(spots_in_range(start, grid, steps))


def part2(input_path: str = INPUT_PATH, steps: int = 26501365) -> int:
    grid = parse_grid(read_as_lines(input_path))
    start = find_symbol(grid, "S")
    size = max(c[1] for c in grid.keys()) + 1
    edge = size // 2

    # solve three first iterations for quadratic solver
    spots = [spots_in_range(start, grid, (edge + i * size)) for i in range(3)]
    num_spots = list(map(len, spots))

    q = quad(num_spots, (steps - edge) // size)

    return q
