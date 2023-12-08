import math
import os
import re

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def parse_node_map(lines: list[str]) -> dict[str, tuple[str, str]]:
    node_map = {}
    for line in lines:
        node_ids = re.findall(r"\w+", line)
        node_map[node_ids[0]] = node_ids[1], node_ids[2]

    return node_map


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    instructions = lines[0]
    node_map = parse_node_map(lines[2:])

    at, steps = "AAA", 0

    while True:
        idx = steps % len(instructions)

        at, steps = node_map[at][0 if instructions[idx] == "L" else 1], steps + 1

        if at == "ZZZ":
            break

    return steps


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    instructions = lines[0]
    node_map = parse_node_map(lines[2:])

    def steps_to_z(starting_id: str) -> int:
        at, steps = starting_id, 0

        while True:
            idx = steps % len(instructions)
            at, steps = node_map[at][0 if instructions[idx] == "L" else 1], steps + 1

            if at.endswith("Z"):
                break

        return steps

    starting_nodes: list[str] = [key for key in node_map.keys() if key.endswith("A")]

    steps_from_starts = [steps_to_z(node) for node in starting_nodes]

    return math.lcm(*steps_from_starts)
