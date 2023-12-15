import copy
import os
from typing import Iterator

from aoc2023.day11 import transpose
from aoc2023.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Pattern = list[str]


def overlap_matches(a: Pattern, b: Pattern) -> bool:
    overlap = min(len(a), len(b))

    return a[:overlap] == b[:overlap]


def h_reflections(p: Pattern) -> Iterator[int]:
    for i in range(1, len(p)):
        folded = list(reversed(p[:i]))
        left = p[i:]

        if overlap_matches(folded, left):
            yield i


def v_reflections(p: Pattern) -> Iterator[int]:
    yield from h_reflections(transpose(p))


def part1(input_path: str = INPUT_PATH) -> int:
    string = read_as_string(input_path)

    patterns: list[Pattern] = [p.strip().split("\n") for p in string.split("\n\n")]

    v_refs = filter(None, (next(v_reflections(p), None) for p in patterns))
    h_refs = filter(None, (next(h_reflections(p), None) for p in patterns))

    return sum(v_refs) + 100 * sum(h_refs)


def solve_pattern(p: Pattern) -> tuple[int, int]:
    orig_v = next(v_reflections(p), None)
    orig_h = next(h_reflections(p), None)

    for y, row in enumerate(p):
        for x, char in enumerate(row):
            pc = copy.deepcopy(p)
            replacement = "." if char == "#" else "#"
            pc[y] = row[:x] + replacement + row[x + 1 :]

            new_v = next((v for v in v_reflections(pc) if v != orig_v), None)
            if new_v:
                return new_v, 0

            new_h = next((h for h in h_reflections(pc) if h != orig_h), None)
            if new_h:
                return 0, new_h

    return 0, 0


def part2(input_path: str = INPUT_PATH) -> int:
    string = read_as_string(input_path)

    patterns: list[Pattern] = [p.strip().split("\n") for p in string.split("\n\n")]

    ver_sum = 0
    hor_sum = 0

    for p in patterns:
        new_v, new_h = solve_pattern(p)
        ver_sum += new_v
        hor_sum += new_h

    return ver_sum + 100 * hor_sum
