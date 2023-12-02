import os
import re

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def _to_int(in_str: str) -> str:
    if in_str.isdigit():
        return in_str

    if in_str in digit_map:
        return digit_map[in_str]

    raise ValueError("not a known digit")


def num_digits(in_str: str) -> list[str]:
    digit_pattern = r"\d"
    matches_list = [match.group() for match in re.finditer(digit_pattern, in_str)]

    if not matches_list:
        raise ValueError("no digits found")

    return matches_list


def any_digits(in_str: str) -> list[str]:
    digit_pattern = "|".join([r"\d", *digit_map.keys()])
    first_match = re.match(rf".*?({digit_pattern}).*", in_str)
    last_match = re.match(rf".*({digit_pattern}).*?", in_str)

    if not first_match:
        raise ValueError("no digits found")

    first_digit = _to_int(first_match.groups()[0])

    if not last_match:
        return [first_digit, first_digit]

    last_digit = _to_int(last_match.groups()[0])
    return [first_digit, last_digit]


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    digit_lists = [num_digits(line) for line in lines]

    total = sum((int(d_list[0] + d_list[-1]) for d_list in digit_lists))

    return total


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    digit_lists = [any_digits(line) for line in lines]

    total = sum((int(d_list[0] + d_list[-1]) for d_list in digit_lists))

    return total
