import os
import re
from itertools import repeat

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def generate_alternatives(record: str) -> list[str]:
    # print(record)
    first_char = record[0]
    alts: list[str] = [first_char] if not first_char == "?" else [".", "#"]
    for char in record[1:]:
        if char == "?":
            alts = [*(a + "#" for a in alts), *(a + "." for a in alts)]
        else:
            alts = [a + char for a in alts]

    # print(alts)
    return alts


def build_pattern(groups: list[int]) -> str:
    # Groups 1,1,3 separated by dots: r'\.*#{1}\.+#{1}\.+#{3}\.*
    group_patterns = [f"#{{{g}}}" for g in groups]
    separator = r"\.+"
    cap = r"\.*"

    # print(groups, f"{cap}{separator.join(group_patterns)}{cap}")
    return f"^{cap}{separator.join(group_patterns)}{cap}$"


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)
    valid_alternatives = 0

    for line in lines:
        record, group_str = line.split(" ")

        alternatives = generate_alternatives(record)
        groups = [int(g) for g in group_str.split(",")]

        pattern = build_pattern(groups)

        matches = list(filter(lambda s: re.match(pattern, s), alternatives))
        # print(matches)
        num_matches = len(matches)
        # print(line, num_matches)

        valid_alternatives += num_matches

    return valid_alternatives


def solver(
    record: str,
    groups: list[int],
    record_idx,
    group_idx,
    block_size: int,
    cache: dict | None = None,
) -> int:
    if cache is None:
        cache = {}

    key = (record_idx, group_idx, block_size)
    if key in cache:
        return cache[key]

    # Reaching the end of the record
    if record_idx == len(record):
        # All groups have been matched, no current ongoing block -> path is valid
        if group_idx == len(groups) and block_size == 0:
            return 1
        # Currently on last group, current block matches the group -> path is valid
        elif group_idx == len(groups) - 1 and groups[group_idx] == block_size:
            return 1
        # All groups have not been matched successfully -> not a valid path
        else:
            return 0

    branch_total = 0

    # Branch out for . and # alternatives
    for char in [".", "#"]:
        if record[record_idx] == char or record[record_idx] == "?":
            # Good string, not in the middle of block of bad springs
            if char == "." and block_size == 0:
                # move to next char, same group
                branch_total += solver(
                    record, groups, record_idx + 1, group_idx, 0, cache
                )
            # Good spring, current block matches the current expected group
            elif (
                char == "."
                and block_size > 0
                and group_idx < len(groups)
                and groups[group_idx] == block_size
            ):
                # Move to next char, next group, reset the block count
                branch_total += solver(
                    record, groups, record_idx + 1, group_idx + 1, 0, cache
                )
            # Bad spring
            elif char == "#":
                # Move to next char, increment block count
                branch_total += solver(
                    record, groups, record_idx + 1, group_idx, block_size + 1, cache
                )
    cache[key] = branch_total

    return branch_total


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)
    valid_alternatives = 0

    for n, line in enumerate(lines):
        record, group_str = line.split(" ")
        record = "?".join(repeat(record, 5))
        group_str = ",".join(repeat(group_str, 5))

        groups = [int(g) for g in group_str.split(",")]

        score = solver(record, groups, 0, 0, 0)

        valid_alternatives += score

    return valid_alternatives
