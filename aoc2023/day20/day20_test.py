import os

import pytest

from aoc2023.day20 import Conjunction, FlipFlop, Pulse, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")
INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class TestFlipFlow:
    @pytest.mark.parametrize("state", [Pulse.high, Pulse.low])
    def test_high_pulse(self, state):
        ff = FlipFlop("ff", ["one", "two", "three"], state=state)

        assert ff.pulse_in(("anywhere", Pulse.high)) == []

    @pytest.mark.parametrize("state", [Pulse.high, Pulse.low])
    def test_low_pulse(self, state):
        ff = FlipFlop("ff", ["one", "two", "three"], state=state)

        assert ff.pulse_in(("anywhere", Pulse.low)) == [
            ("one", ("ff", state.inverse())),
            ("two", ("ff", state.inverse())),
            ("three", ("ff", state.inverse())),
        ]
        assert ff.state == state.inverse()


class TestConjunction:
    def test_remembers_pulses(self):
        c = Conjunction("c", ["one", "two", "three"])
        assert c.inputs == {}

        c.pulse_in(("1", Pulse.low))
        assert c.inputs == {"1": Pulse.low}

        c.pulse_in(("1", Pulse.high))
        assert c.inputs == {"1": Pulse.high}

        c.pulse_in(("15", Pulse.high))
        assert c.inputs == {"1": Pulse.high, "15": Pulse.high}

    def test_output_when_all_high(self):
        c = Conjunction("c", ["one", "two", "three"], {"previous_input": Pulse.high})

        assert c.pulse_in(("source", Pulse.high)) == [
            ("one", ("c", Pulse.low)),
            ("two", ("c", Pulse.low)),
            ("three", ("c", Pulse.low)),
        ]

    def test_output_when_any_low(self):
        c = Conjunction("c", ["four", "five", "six"], {"previous_input": Pulse.high})

        assert c.pulse_in(("source", Pulse.low)) == [
            ("four", ("c", Pulse.high)),
            ("five", ("c", Pulse.high)),
            ("six", ("c", Pulse.high)),
        ]

        c = Conjunction("c", ["seven", "eight", "nine"], {"previous_input": Pulse.low})

        assert c.pulse_in(("source", Pulse.high)) == [
            ("seven", ("c", Pulse.high)),
            ("eight", ("c", Pulse.high)),
            ("nine", ("c", Pulse.high)),
        ]


def test_part1():
    assert part1(TEST_INPUT_PATH) == 32000000
    assert part1(TEST_INPUT_2_PATH) == 11687500


def test_part2():
    assert part2(INPUT_PATH) == 253302889093151
