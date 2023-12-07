import os
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from itertools import combinations_with_replacement

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class HandType(Enum):
    five_of_a_kind = 0
    four_of_a_kind = 1
    full_house = 2
    three_of_a_kind = 3
    two_pair = 4
    one_pair = 5
    high_card = 6


@dataclass
class Hand:
    cards: str
    bid: int

    @property
    def card_label_order(self) -> str:
        return "AKQJT98765432"

    @cached_property
    def card_counts(self) -> Counter[str]:
        return Counter(self.cards)

    @cached_property
    def type(self) -> HandType:
        if len(self.card_counts.keys()) == 1:
            return HandType.five_of_a_kind

        if max(self.card_counts.values()) == 4:
            return HandType.four_of_a_kind

        if sorted(self.card_counts.values()) == [2, 3]:
            return HandType.full_house

        if max(self.card_counts.values()) == 3:
            return HandType.three_of_a_kind

        if sorted(self.card_counts.values()) == [1, 2, 2]:
            return HandType.two_pair

        if sorted(self.card_counts.values()) == [1, 1, 1, 2]:
            return HandType.one_pair

        return HandType.high_card

    def __lt__(self, other: "Hand") -> bool:
        if self.type.value < other.type.value:
            return True

        # Break ties using card label values
        if self.type.value == other.type.value:
            for [a, b] in zip(self.cards, other.cards):
                a_label = self.card_label_order.index(a)
                b_label = self.card_label_order.index(b)
                if a_label < b_label:
                    return True
                if a_label > b_label:
                    break

        return False


class JokerHand(Hand):
    @property
    def card_label_order(self) -> str:
        return "AKQT98765432J"

    def possible_hands(self) -> list[Hand]:
        non_jokers = self.cards.replace("J", "")
        num_jokers = len(self.cards) - len(non_jokers)

        possible_replacements = [
            "".join(combo)
            for combo in combinations_with_replacement("AKQT98765432", num_jokers)
        ]
        return [
            Hand(cards=non_jokers + replacement, bid=self.bid)
            for replacement in possible_replacements
        ]

    @cached_property
    def type(self) -> HandType:
        possible_hands = self.possible_hands()
        best_hand: Hand = sorted(possible_hands)[0]
        return best_hand.type


def parse_hand(line: str) -> Hand:
    parts = line.split()
    return Hand(cards=parts[0], bid=int(parts[1]))


def parse_joker_hand(line: str) -> JokerHand:
    parts = line.split()
    return JokerHand(cards=parts[0], bid=int(parts[1]))


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    hands = [parse_hand(line) for line in lines]
    ranked_hands_from_weakest = sorted(hands, reverse=True)

    winnings = [
        rank * hand.bid for rank, hand in enumerate(ranked_hands_from_weakest, 1)
    ]

    return sum(winnings)


def part2(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    hands = [parse_joker_hand(line) for line in lines]
    ranked_hands_from_weakest = sorted(hands, reverse=True)

    winnings = [
        rank * hand.bid for rank, hand in enumerate(ranked_hands_from_weakest, 1)
    ]

    return sum(winnings)
