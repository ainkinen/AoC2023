import os
import re
from dataclasses import dataclass
from typing import Callable

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Counts:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: int
    reveals: list[Counts]


def parse_reveal(line: str) -> Counts:
    pattern = r"(\d+) (red|green|blue)"
    matches = re.findall(pattern, line)

    red, green, blue = 0, 0, 0

    for match in matches:
        count = int(match[0])
        color = match[1]

        match color:
            case "red":
                red = count
            case "green":
                green = count
            case "blue":
                blue = count
            case _:
                raise ValueError("unknown color revealed")

    return Counts(red=red, green=green, blue=blue)


def parse_id(line: str) -> int:
    pattern = r"\d+"
    match = re.search(pattern, line)

    if not match:
        raise ValueError("could not parse the game id")

    return int(match.group())


def parse_game(line: str) -> Game:
    [id_side, reveals_side] = line.split(":", 1)

    return Game(
        id=parse_id(id_side),
        reveals=[parse_reveal(r) for r in reveals_side.split(";")],
    )


def reveal_is_max(max_counts: Counts) -> Callable[[Counts], bool]:
    def is_max(reveal: Counts) -> bool:
        return (
            reveal.red <= max_counts.red
            and reveal.green <= max_counts.green
            and reveal.blue <= max_counts.blue
        )

    return is_max


def min_needed_counts(reveals: list[Counts]) -> Counts:
    return Counts(
        red=max(r.red for r in reveals),
        green=max(r.green for r in reveals),
        blue=max(r.blue for r in reveals),
    )


def part1(input_path: str = INPUT_PATH) -> int:
    rule = reveal_is_max(Counts(red=12, green=13, blue=14))

    lines = read_as_lines(input_path)
    games = [parse_game(line) for line in lines]

    filtered_games = [game for game in games if all(map(rule, game.reveals))]

    ids = [game.id for game in filtered_games]

    return sum(ids)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)
    games = [parse_game(line) for line in lines]

    min_counts = [min_needed_counts(game.reveals) for game in games]

    powers = [c.red * c.green * c.blue for c in min_counts]

    return sum(powers)
