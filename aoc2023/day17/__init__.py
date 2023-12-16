import heapq
import os

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Grid = dict[tuple[int, int], int]
Coord = tuple[int, int]  # y,x


def read_grid(input_path: str) -> Grid:
    lines = read_as_lines(input_path)
    return {(y, x): int(h) for y, line in enumerate(lines) for x, h in enumerate(line)}


def solver(
    grid: Grid,
    start: Coord,
    goal: Coord,
    min_steps: int,
    max_steps: int,
) -> int:
    # heat, loc, prev_step_delta
    queue: list[tuple[int, Coord, Coord]] = [(0, start, (0, 0))]

    # loc, prev_step_delta
    seen: set[tuple[Coord, Coord]] = set()

    while queue:
        heat, loc, prev_step_delta = heapq.heappop(queue)

        if loc == goal:
            return heat

        if (loc, prev_step_delta) in seen:
            continue

        seen.add((loc, prev_step_delta))

        # Loop only turns
        back_or_front = {prev_step_delta, (-prev_step_delta[0], -prev_step_delta[1])}
        turns = {(0, 1), (0, -1), (1, 0), (-1, 0)} - back_or_front
        for turn_dy, turn_dx in turns:
            (step_y, step_x), step_heat = loc, heat

            # Loop forward steps
            for i in range(1, max_steps + 1):
                step_y, step_x = step_y + turn_dy, step_x + turn_dx
                if (step_y, step_x) in grid:
                    step_heat += grid[(step_y, step_x)]
                    if i >= min_steps:
                        heapq.heappush(
                            queue, (step_heat, (step_y, step_x), (turn_dy, turn_dx))
                        )

    raise Exception("end not found")


def part1(input_path: str = INPUT_PATH) -> int:
    grid = read_grid(input_path)

    start: Coord = min(grid)
    goal: Coord = max(grid)

    return solver(grid, start, goal, 1, 3)


def part2(input_path: str = INPUT_PATH) -> int:
    grid = read_grid(input_path)

    start: Coord = min(grid)
    goal: Coord = max(grid)

    return solver(grid, start, goal, 4, 10)
