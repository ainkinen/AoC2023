import os
import re
from functools import reduce

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def _parse_numbers(in_str: str) -> list[int]:
    return [int(number) for number in re.findall(r"\d+", in_str)]


def travel_distance(press_time: int, total_time: int) -> int:
    speed = press_time
    travel_time = total_time - press_time
    return speed * travel_time


def get_winning_presses(race_time: int, record_distance: int) -> list[int]:
    possible_presses = range(race_time)

    return [
        press_time
        for press_time in possible_presses
        if travel_distance(press_time, race_time) > record_distance
    ]


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    times = _parse_numbers(lines[0])
    distances = _parse_numbers(lines[1])

    winning_runs: list[list[int]] = [
        get_winning_presses(time, distance)
        for (time, distance) in zip(times, distances)
    ]

    margins_of_error = [len(run) for run in winning_runs]

    return reduce(lambda acc, cur: acc * cur, margins_of_error)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    times = _parse_numbers(lines[0].replace(" ", ""))
    distances = _parse_numbers(lines[1].replace(" ", ""))

    winning_runs: list[list[int]] = [
        get_winning_presses(time, distance)
        for (time, distance) in zip(times, distances)
    ]

    margins_of_error = [len(run) for run in winning_runs]

    return reduce(lambda acc, cur: acc * cur, margins_of_error)
