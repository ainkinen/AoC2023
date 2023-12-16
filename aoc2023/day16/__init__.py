import os
from itertools import chain

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


Grid = list[str]
Coord = tuple[int, int]  # y, x
Head = tuple[str, Coord]


def next_heads(head: Head, grid: Grid) -> list[Head]:
    direction, (y, x) = head
    symbol = grid[y][x]

    match symbol:
        case ".":
            if direction == "U":
                return [(direction, (y - 1, x))]
            if direction == "D":
                return [(direction, (y + 1, x))]
            if direction == "L":
                return [(direction, (y, x - 1))]
            if direction == "R":
                return [(direction, (y, x + 1))]
            raise ValueError(f"Unknown direction {direction}")

        case "|":
            if direction == "U":
                return [(direction, (y - 1, x))]
            if direction == "D":
                return [(direction, (y + 1, x))]
            if direction in "LR":
                return [
                    ("U", (y - 1, x)),
                    ("D", (y + 1, x)),
                ]
            raise ValueError(f"Unknown direction {direction}")

        case "-":
            if direction == "L":
                return [(direction, (y, x - 1))]
            if direction == "R":
                return [(direction, (y, x + 1))]
            if direction in "UD":
                return [
                    ("L", (y, x - 1)),
                    ("R", (y, x + 1)),
                ]
            raise ValueError(f"Unknown direction {direction}")

        case "/":
            if direction == "U":
                return [("R", (y, x + 1))]
            if direction == "D":
                return [("L", (y, x - 1))]
            if direction == "L":
                return [("D", (y + 1, x))]
            if direction == "R":
                return [("U", (y - 1, x))]
            raise ValueError(f"Unknown direction {direction}")

        case "\\":
            if direction == "U":
                return [("L", (y, x - 1))]
            if direction == "D":
                return [("R", (y, x + 1))]
            if direction == "L":
                return [("U", (y - 1, x))]
            if direction == "R":
                return [("D", (y + 1, x))]
            raise ValueError(f"Unknown direction {direction}")

        case _:
            raise ValueError(f"Unknown symbol {symbol}")


def solve(grid: Grid, start: Head) -> int:
    min_y, max_y = 0, len(grid) - 1
    min_x, max_x = 0, len(grid[0]) - 1

    def inbounds(c: Coord) -> bool:
        return (min_y <= c[0] <= max_y) and (min_x <= c[1] <= max_x)

    path: set[Head] = {start}
    heads: list[Head] = [start]
    while heads:
        heads = list(chain(*(next_heads(head, grid) for head in heads)))

        # kill out of bounds beams
        heads = list(filter(lambda h: inbounds(h[1]), heads))

        # kill loops
        heads = list(filter(lambda h: h not in path, heads))

        for head in heads:
            path.add(head)

    return len(set(head[1] for head in path))


def part1(input_path: str = INPUT_PATH) -> int:
    grid = read_as_lines(input_path)
    start = ("R", (0, 0))  # Start at top-left heading right

    return solve(grid, start)


def part2(input_path: str = INPUT_PATH) -> int:
    grid = read_as_lines(input_path)

    min_y, max_y = 0, len(grid) - 1
    min_x, max_x = 0, len(grid[0]) - 1

    starts: list[Head] = [
        *(("D", (min_y, x)) for x in range(max_x + 1)),
        *(("U", (max_y, x)) for x in range(max_x + 1)),
        *(("R", (y, min_x)) for y in range(max_y + 1)),
        *(("L", (y, max_x)) for y in range(max_y + 1)),
    ]

    results = [solve(grid, start) for start in starts]

    return max(results)
