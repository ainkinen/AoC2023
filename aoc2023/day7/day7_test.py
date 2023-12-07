import os

from aoc2023.day7 import Hand, HandType, JokerHand, parse_hand, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


def test_parse_hand():
    assert parse_hand("32T3K 765") == Hand(cards="32T3K", bid=765)
    assert parse_hand("T55J5 684") == Hand(cards="T55J5", bid=684)
    assert parse_hand("KK677 28") == Hand(cards="KK677", bid=28)
    assert parse_hand("KTJJT 220") == Hand(cards="KTJJT", bid=220)
    assert parse_hand("QQQJA 483") == Hand(cards="QQQJA", bid=483)


class TestHand:
    def test_type(self):
        assert Hand(cards="32T3K", bid=765).type == HandType.one_pair
        assert Hand(cards="T55J5", bid=684).type == HandType.three_of_a_kind
        assert Hand(cards="KK677", bid=28).type == HandType.two_pair
        assert Hand(cards="KTJJT", bid=220).type == HandType.two_pair
        assert Hand(cards="QQQJA", bid=483).type == HandType.three_of_a_kind
        assert Hand(cards="TTTTT", bid=28).type == HandType.five_of_a_kind
        assert Hand(cards="TTTAT", bid=28).type == HandType.four_of_a_kind
        assert Hand(cards="TAATT", bid=28).type == HandType.full_house
        assert Hand(cards="23456", bid=28).type == HandType.high_card


class TestJokerHand:
    async def test_possible_hands(self):
        assert JokerHand(cards="T55J5", bid=0).possible_hands() == [
            Hand(cards="T555A", bid=0),
            Hand(cards="T555K", bid=0),
            Hand(cards="T555Q", bid=0),
            Hand(cards="T555T", bid=0),
            Hand(cards="T5559", bid=0),
            Hand(cards="T5558", bid=0),
            Hand(cards="T5557", bid=0),
            Hand(cards="T5556", bid=0),
            Hand(cards="T5555", bid=0),
            Hand(cards="T5554", bid=0),
            Hand(cards="T5553", bid=0),
            Hand(cards="T5552", bid=0),
        ]

    async def test_type(self):
        assert JokerHand(cards="T55J5", bid=0).type == HandType.four_of_a_kind


def test_part1():
    assert part1(TEST_INPUT_PATH) == 6440


def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 5905
