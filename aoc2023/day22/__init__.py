import os
from collections import defaultdict
from copy import deepcopy
from itertools import product
from queue import Queue
from typing import Iterable

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Coord = tuple[int, int, int]  # x,y,z
Space = dict[Coord, int]  # coord -> brick idx
Brick = tuple[range, range, range]  # range_x,range_y,range_z
Graph = dict[int, set[int]]  # idx -> set[idx]


def coords(b: Brick) -> Iterable[Coord]:
    yield from product(b[0], b[1], b[2])


def parse_coord(in_str: str) -> Coord:
    x, y, z = map(int, in_str.split(","))
    return x, y, z


def parse_brick(line: str) -> Brick:
    start, end = map(parse_coord, line.split("~"))

    return (
        range(start[0], end[0] + 1),
        range(start[1], end[1] + 1),
        range(start[2], end[2] + 1),
    )


def fill_space(space: Space, b: Brick, idx: int):
    for coord in coords(b):
        space[coord] = idx


def clear_space(space: Space, b: Brick):
    for coord in coords(b):
        del space[coord]


def part1(input_path: str = INPUT_PATH) -> int:
    # sorted from bottom to top for easier iteration
    bricks = sorted(
        [parse_brick(line) for line in read_as_lines(input_path)],
        key=lambda brick: brick[2].start,
    )

    # fill the initial brick space
    space: Space = defaultdict(None)
    for idx, b in enumerate(bricks):
        fill_space(space, b, idx)

    supported_by: Graph = defaultdict(set)  # idx, set[supports]

    for idx, b in enumerate(bricks):
        while True:
            # loop until brick cant move any lower
            rx, ry, rz = b

            if rz.start == 1:
                # reached the bottom
                break

            new_rz = range(rz.start - 1, rz.stop - 1)

            for x in rx:
                for y in ry:
                    block_below = x, y, new_rz.start
                    if block_below in space:
                        supported_by[idx].add(space[block_below])

            if len(supported_by[idx]):
                # is supported, cant move
                break

            else:
                # hanging, move one step and continue
                new_b = rx, ry, new_rz
                clear_space(space, b)
                fill_space(space, new_b, idx)
                b = new_b

    # invert support graph
    supports: Graph = defaultdict(set)
    for idx, on_top in supported_by.items():
        for top_idx in on_top:
            supports[top_idx].add(idx)

    destroyable: list[int] = []

    for idx in range(len(bricks)):
        if idx not in supports:
            # the brick does not support any other bricks
            destroyable.append(idx)
            continue

        if all(len(supported_by[b]) > 1 for b in supports[idx]):
            # all supported bricks have other supports
            destroyable.append(idx)
            continue

    return len(destroyable)


def part2(input_path: str = INPUT_PATH) -> int:
    # sorted from bottom to top for easier iteration
    bricks = sorted(
        [parse_brick(line) for line in read_as_lines(input_path)],
        key=lambda brick: brick[2].start,
    )

    # fill the initial brick space
    space: Space = defaultdict(None)
    for idx, b in enumerate(bricks):
        fill_space(space, b, idx)

    supported_by: Graph = defaultdict(set)  # idx, set[supports]

    for idx, b in enumerate(bricks):
        while True:
            # loop until brick cant move any lower
            rx, ry, rz = b

            if rz.start == 1:
                # reached the bottom
                break

            new_rz = range(rz.start - 1, rz.stop - 1)

            for x in rx:
                for y in ry:
                    block_below = x, y, new_rz.start
                    if block_below in space:
                        supported_by[idx].add(space[block_below])

            if len(supported_by[idx]):
                # is supported, cant move
                break

            else:
                # hanging, move one step and continue
                new_b = rx, ry, new_rz
                clear_space(space, b)
                fill_space(space, new_b, idx)
                b = new_b

    # invert support graph
    supports: Graph = defaultdict(set)
    for idx, on_top in supported_by.items():
        for top_idx in on_top:
            supports[top_idx].add(idx)

    def chained_removals(starting_brick_idx: int) -> int:
        # need a copy since supports will be removed
        supported_by_copy = deepcopy(supported_by)
        deletion_queue: Queue[int] = Queue()
        deletion_queue.put(starting_brick_idx)

        destroyed = set()

        while not deletion_queue.empty():
            b_idx = deletion_queue.get()
            destroyed.add(b_idx)

            for s in supports[b_idx]:
                supported_by_copy[s].discard(b_idx)
                if len(supported_by_copy[s]) == 0 and s not in destroyed:
                    deletion_queue.put(s)

        return len(destroyed) - 1  # The first removal is not part of the chain reaction

    return sum((chained_removals(idx) for idx in range(len(bricks))))
