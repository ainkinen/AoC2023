import os

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int]  # y, x
Grid = dict[Coord, str]  # loc, content
Graph = dict[Coord, dict[Coord, int]]  # vertex -> dict[vertex, steps]

valid_directions = {
    ">": [(0, 1)],
    "<": [(0, -1)],
    "^": [(-1, 0)],
    "v": [(1, 0)],
}


def parse_grid(lines: list[str]) -> Grid:
    grid: Grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(y, x)] = char

    return grid


def valid_neighbours(loc: Coord, grid: Grid, slopes_are_slippery: bool) -> set[Coord]:
    y, x = loc
    tile = grid[loc]

    neighbours: set[Coord] = set()

    deltas = (
        valid_directions[tile]
        if tile in valid_directions and slopes_are_slippery
        else [(-1, 0), (1, 0), (0, -1), (0, 1)]
    )
    for delta in deltas:
        new_loc = y + delta[0], x + delta[1]
        if new_loc not in grid:
            continue

        if grid[new_loc] == "#":
            continue

        neighbours.add(new_loc)

    return neighbours


def find_nodes(grid: Grid, slopes_are_slippery: bool) -> set[Coord]:
    nodes: set[Coord] = set()
    for loc in grid.keys():
        if len(valid_neighbours(loc, grid, slopes_are_slippery)) > 2:
            nodes.add(loc)
    return nodes


def find_edges(
    node: Coord, grid: Grid, nodes: set[Coord], slopes_are_slippery: bool
) -> dict[Coord, int]:
    edges: dict[Coord, int] = {}

    active_paths: list[list[Coord]] = [[node]]

    while active_paths:
        cur_path = active_paths.pop()
        head = cur_path[-1]
        prev = cur_path[-2] if len(cur_path) > 1 else None
        next_steps = valid_neighbours(head, grid, slopes_are_slippery) - {
            prev
        }  # no backtracking
        for step in next_steps:
            if step in nodes:
                # end found
                edges[step] = len(cur_path)
                continue

            active_paths.append([*cur_path, step])

    return edges


def build_graph(
    grid: Grid, start: Coord, end: Coord, slopes_are_slippery: bool
) -> Graph:
    nodes = find_nodes(grid, slopes_are_slippery)

    nodes.update({start, end})

    return {v: find_edges(v, grid, nodes, slopes_are_slippery) for v in nodes}


def find_paths(graph: Graph, start: Coord, end: Coord) -> list[list[Coord]]:
    active_paths = [[start]]

    found_paths: list[list[Coord]] = []

    while active_paths:
        cur_path: list[Coord] = active_paths.pop()
        head = cur_path[-1]

        next_nodes = {n for n in graph[head].keys()} - set(cur_path)  # no backlinks

        for node in next_nodes:
            new_path = [*cur_path, node]
            if node == end:
                found_paths.append(new_path)
            else:
                active_paths.append(new_path)

    return found_paths


def get_path_length(path: list[Coord], graph: Graph) -> int:
    edge_lengths: list[int] = []
    for idx in range(1, len(path)):
        from_node = path[idx - 1]
        to_node = path[idx]
        edge_lengths.append(graph[from_node][to_node])

    return sum(edge_lengths)


def solve(input_path: str, slopes_are_slippery: bool) -> int:
    lines = read_as_lines(input_path)
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1

    grid = parse_grid(lines)

    start = (0, 1)
    end = (max_y, max_x - 1)
    graph = build_graph(grid, start, end, slopes_are_slippery)

    paths = find_paths(graph, start, end)

    path_lengths = [get_path_length(path, graph) for path in paths]

    return max(path_lengths)


def part1(input_path: str = INPUT_PATH) -> int:
    return solve(input_path, True)


def part2(input_path: str = INPUT_PATH) -> int:
    return solve(input_path, False)
