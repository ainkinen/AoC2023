import os
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum
from math import lcm

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class Pulse(Enum):
    high = 1
    low = 0

    def inverse(self):
        if self == Pulse.high:
            return Pulse.low

        return Pulse.high


Signal = tuple[str, Pulse]  # source, pulse
Output = tuple[str, Signal]  # to, signal


@dataclass
class Module(ABC):
    name: str
    outputs: list[str]

    @abstractmethod
    def pulse_in(self, signal: Signal) -> list[Output]:
        ...


@dataclass
class Button(Module):
    def pulse_in(self, signal: Signal) -> list[Output]:
        return [(o, (self.name, Pulse.low)) for o in self.outputs]


@dataclass
class Broadcaster(Module):
    def pulse_in(self, signal: Signal) -> list[Output]:
        return [(o, (self.name, signal[1])) for o in self.outputs]


@dataclass
class FlipFlop(Module):
    state: Pulse = Pulse.low

    def pulse_in(self, signal: Signal) -> list[Output]:
        source, pulse = signal

        if pulse == Pulse.high:
            return []

        # flips
        self.state = self.state.inverse()
        return [(o, (self.name, self.state)) for o in self.outputs]


@dataclass
class Conjunction(Module):
    inputs: dict[str, Pulse] = field(default_factory=dict)

    def pulse_in(self, signal: Signal) -> list[Output]:
        source, pulse = signal
        self.inputs[source] = pulse

        output_pulse = (
            Pulse.low
            if all(v == Pulse.high for v in self.inputs.values())
            else Pulse.high
        )

        return [(o, (self.name, output_pulse)) for o in self.outputs]


def parse_module(line: str) -> tuple[str, Module]:
    left, right = line.split(" -> ")
    outputs = [o.strip() for o in right.split(",")]

    if left == "broadcaster":
        return left, Broadcaster("broadcaster", outputs)

    kind, name = left[:1], left[1:]

    if kind == "%":
        return name, FlipFlop(name, outputs)

    if kind == "&":
        return name, Conjunction(name, outputs)

    raise Exception(f"Unknown module {line}")


def part1(input_path: str = INPUT_PATH) -> int:
    modules: dict[str, Module] = dict(
        parse_module(line) for line in read_as_lines(input_path)
    )

    # Collect inputs for conjunctions
    for source_module in modules.values():
        for output_name in source_module.outputs:
            if output_name not in modules:
                continue
            output_module = modules[output_name]
            if isinstance(output_module, Conjunction):
                output_module.inputs[source_module.name] = Pulse.low

    modules["button"] = Button("button", ["broadcaster"])

    signals: deque[Output] = deque()

    lows = 0
    highs = 0
    for i in range(1000):
        signals.append(("button", ("elf", Pulse.low)))
        while signals:
            name, signal = signals.popleft()
            if name not in modules:
                continue

            outputs = modules[name].pulse_in(signal)

            pulse_counts: Counter[Pulse] = Counter([o[1][1] for o in outputs])
            lows += pulse_counts[Pulse.low]
            highs += pulse_counts[Pulse.high]

            signals.extend(outputs)

    return lows * highs


def part2(input_path: str = INPUT_PATH) -> int:
    modules: dict[str, Module] = dict(
        parse_module(line) for line in read_as_lines(input_path)
    )

    # Collect inputs for conjunctions
    for source_module in modules.values():
        for output_name in source_module.outputs:
            if output_name not in modules:
                continue
            output_module = modules[output_name]
            if isinstance(output_module, Conjunction):
                output_module.inputs[source_module.name] = Pulse.low

    modules["button"] = Button("button", ["broadcaster"])

    signals: deque[Output] = deque()

    counter_outputs = {
        "xl": 0,
        "gp": 0,
        "xp": 0,
        "ln": 0,
    }

    presses = 0
    while any(v == 0 for v in counter_outputs.values()):
        signals.append(("button", ("elf", Pulse.low)))
        presses += 1

        while signals:
            name, signal = signals.popleft()
            if name not in modules:
                continue

            outputs = modules[name].pulse_in(signal)

            for output in outputs:
                destination, (source, pulse) = output
                if destination in counter_outputs.keys() and pulse == Pulse.low:
                    counter_outputs[destination] = presses

            signals.extend(outputs)

    return lcm(*counter_outputs.values())
