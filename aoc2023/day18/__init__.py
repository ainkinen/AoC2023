import os
import re

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Instruction = tuple[str, int]  # direction, steps
Coord = tuple[int, int]  # y, x

encoded_directions = {"0": "R", "1": "D", "2": "L", "3": "U"}


def parse_instruction(line: str) -> Instruction:
    p = r"(\w) (\d+) \(#(\w+)\)"
    match = re.match(p, line)
    if not match:
        raise Exception(f"Invalid line {line}")

    return match.groups()[0], int(match.groups()[1])


def parse_hex_instruction(line: str) -> Instruction:
    p = r"\w \d+ \(#(\w{5})(\w)\)"
    match = re.match(p, line)
    if not match:
        raise Exception(f"Invalid line {line}")

    return encoded_directions[match.groups()[1]], int(match.groups()[0], 16)


def shoelace_area(boundary: list[Coord]) -> int:
    # Shoelace algorithm
    num_segments = len(boundary) - 1
    area = [
        (boundary[i + 1][0] - boundary[i][0]) * (boundary[i + 1][1] + boundary[i][1])
        for i in range(num_segments)
    ]
    return abs(sum(area) // 2)


def solve(instructions: list[Instruction]) -> int:
    loc = (0, 0)
    turns: list[Coord] = [loc]
    len_trench: int = 0
    for ins in instructions:
        direction, step = ins
        y, x = loc
        if direction == "U":
            loc = y - step, x
        elif direction == "D":
            loc = y + step, x
        elif direction == "L":
            loc = y, x - step
        elif direction == "R":
            loc = y, x + step

        turns.append(loc)
        len_trench += step
        continue

    # Pick's theorem
    return shoelace_area(turns) + (len_trench // 2) + 1


def part1(input_path: str = INPUT_PATH) -> int:
    instructions = [parse_instruction(line) for line in read_as_lines(input_path)]
    return solve(instructions)


def part2(input_path: str = INPUT_PATH) -> int:
    hex_instructions = [
        parse_hex_instruction(line) for line in read_as_lines(input_path)
    ]

    return solve(hex_instructions)
