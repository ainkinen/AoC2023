import os
import re
from dataclasses import dataclass
from itertools import chain

from aoc2023.utils.chunker import chunk
from aoc2023.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __len__(self):
        return self.end - self.start


@dataclass(frozen=True)
class Mapping:
    source_range_start: int
    dest_range_start: int
    range_len: int

    @property
    def source_range_end(self) -> int:
        return self.source_range_start + self.range_len - 1

    def convert(self, value: int) -> int:
        if not self.covers(value):
            # Input not in mapping range
            raise ValueError("not in mapping range")

        return self.dest_range_start + value - self.source_range_start

    def covers(self, value: int) -> bool:
        return self.source_range_start <= value <= self.source_range_end


def _parse_mappings(lines: list[str]) -> list[Mapping]:
    mappers: list[Mapping] = []

    for line in lines:
        [dest_start, source_start, range_len] = line.split(" ")
        mappers.append(
            Mapping(
                source_range_start=int(source_start),
                dest_range_start=int(dest_start),
                range_len=int(range_len),
            )
        )

    return mappers


def first_result(value: int, mappings: list[Mapping]) -> int:
    for mapping in mappings:
        if mapping.covers(value):
            return mapping.convert(value)

    return value


def part1(input_path: str = INPUT_PATH) -> int:
    input_str = read_as_string(input_path)

    numerical_section_pattern = r"\d[\d|\s]*\d"

    numerical_sections = re.findall(numerical_section_pattern, input_str)
    seeds = [int(s) for s in numerical_sections[0].split(" ")]

    steps: list[list[Mapping]] = [
        _parse_mappings(section.split("\n")) for section in numerical_sections[1:]
    ]

    final_locations: list[int] = []
    for seed in seeds:
        value = seed
        for mappings in steps:
            value = first_result(value, mappings)

        final_locations.append(value)

    return min(final_locations)


def mapped_ranges(rng: Range, mappings: list[Mapping]) -> list[Range]:
    pointer = rng.start
    new_ranges: list[Range] = []

    sorted_mappings: list[Mapping] = sorted(
        mappings,
        key=lambda m: m.source_range_start,
    )
    while pointer <= rng.end:
        mapping = next(
            (m for m in sorted_mappings if m.source_range_end >= pointer), None
        )
        if not mapping:
            # only unmapped values until range end
            new_range = Range(pointer, rng.end)
        elif pointer < mapping.source_range_start:
            # unmapped range before the next mapping
            new_range = Range(pointer, mapping.source_range_start - 1)
        else:
            # range overlapping with mapping
            new_range = Range(
                mapping.convert(pointer),
                mapping.convert(min(rng.end, mapping.source_range_end)),
            )

        new_ranges.append(new_range)
        pointer += len(new_range) + 1

    return new_ranges


def part2(input_path: str = INPUT_PATH) -> int:
    input_str = read_as_string(input_path)

    numerical_section_pattern = r"\d[\d|\s]*\d"

    numerical_sections = re.findall(numerical_section_pattern, input_str)

    seed_range_entries: list[str] = numerical_sections[0].split(" ")
    seed_ranges: list[Range] = [
        Range(start=int(c[0]), end=int(c[0]) + int(c[1]) - 1)
        for c in chunk(
            seed_range_entries,
            2,
        )
    ]

    steps: list[list[Mapping]] = [
        _parse_mappings(section.split("\n")) for section in numerical_sections[1:]
    ]

    ranges: list[Range] = seed_ranges.copy()
    for step in steps:
        ranges = list(chain.from_iterable([mapped_ranges(r, step) for r in ranges]))

    return min(map(lambda r: r.start, ranges))
