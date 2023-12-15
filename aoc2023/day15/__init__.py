import os
import re
from collections import defaultdict

from aoc2023.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Hashmap = dict[int, dict[str, int]]


def hash_str(in_str: str) -> int:
    val = 0
    for char in in_str:
        val += ord(char)
        val = val * 17
        val = val % 256

    return val


def hash_map(cmd: str, hashmap: Hashmap):
    pattern = r"(\w+)([-|=])(\d?)"
    match = re.match(pattern, cmd)

    if not match:
        raise ValueError(f"Invalid {cmd=}")
    key, op, value_str = match.groups()

    idx = hash_str(key)

    match op:
        case "-":
            if key in hashmap[idx]:
                del hashmap[idx][key]
            if not len(hashmap[idx]):
                del hashmap[idx]
            return

        case "=":
            hashmap[idx][key] = int(value_str)
            return

        case _:
            raise KeyError(f"Unknown op type {op}")


def part1(input_path: str = INPUT_PATH) -> int:
    line = read_as_string(input_path).strip()
    steps = line.split(",")

    return sum(hash_str(s) for s in steps)


def part2(input_path: str = INPUT_PATH) -> int:
    line = read_as_string(input_path).strip()
    steps = line.split(",")

    m: Hashmap = defaultdict(dict)

    for s in steps:
        hash_map(s, m)

    total = 0
    for box_i, d in m.items():
        for slot, focal_length in enumerate(d.values(), 1):
            total += (box_i + 1) * slot * focal_length

    return total
