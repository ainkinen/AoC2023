import os
import re
from collections import defaultdict
from dataclasses import dataclass

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass(frozen=True)
class Card:
    id: int
    lucky_numbers: set[int]
    numbers: set[int]

    @property
    def hits(self) -> set[int]:
        return self.lucky_numbers.intersection(self.numbers)

    @property
    def points(self) -> int:
        if not len(self.hits):
            return 0
        return 2 ** (len(self.hits) - 1)

    @property
    def new_cards(self) -> set[int]:
        return set(
            range(
                self.id + 1,
                self.id + len(self.hits) + 1,
            )
        )


def _parse_numbers(line: str) -> list[int]:
    return [int(g.group()) for g in re.finditer(r"(\d+)", line)]


def parse_card(line: str) -> Card:
    [id_part, numbers_part] = line.split(":", 1)

    id_match = re.search(r"\d+", id_part)
    if not id_match:
        raise ValueError(f"Id not found in {id_part=}")

    [winning_numbers_str, numbers_str] = numbers_part.split("|", 1)

    return Card(
        id=int(id_match.group()),
        lucky_numbers=set(_parse_numbers(winning_numbers_str)),
        numbers=set(_parse_numbers(numbers_str)),
    )


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    cards = [parse_card(line) for line in lines]

    return sum(c.points for c in cards)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    cards = [parse_card(line) for line in lines]

    counts: dict[int, int] = defaultdict(int)

    for card in cards:
        # We always have the original
        counts[card.id] += 1

        # New cards are added times the amount of current card
        for new_card_id in card.new_cards:
            # "Cards will never make you copy a card past the end of the table."
            if new_card_id <= len(cards):
                counts[new_card_id] += counts[card.id]

    return sum(counts.values())
