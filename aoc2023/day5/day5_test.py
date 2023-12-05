import os

import pytest

from aoc2023.day5 import Mapping, Range, mapped_ranges, part1, part2

TEST_INPUT_PATH = os.path.join(os.path.dirname(__file__), "test_input.txt")
TEST_INPUT_2_PATH = os.path.join(os.path.dirname(__file__), "test_input_2.txt")


class TestMappingConvert:
    empty_mapping = Mapping(source_range_start=2, dest_range_start=1, range_len=0)

    mapper1 = Mapping(source_range_start=50, dest_range_start=52, range_len=48)

    mapper2 = Mapping(source_range_start=98, dest_range_start=50, range_len=2)

    async def test_raises_for_values_outside_source_range(self):
        with pytest.raises(ValueError):
            self.empty_mapping.convert(123)

    async def test_returns_mapped_values_for_in_range_input(self):
        assert self.mapper1.convert(50) == 52
        assert self.mapper1.convert(51) == 53
        assert self.mapper1.convert(72) == 74

        assert self.mapper2.convert(98) == 50
        assert self.mapper2.convert(99) == 51


class TestMappedRanges:
    mappings: list[Mapping] = [
        Mapping(0, 50, 10),  # 1
        Mapping(10, 90, 10),  # 2
        Mapping(30, 1000, 10),  # 3
    ]

    def test_return_only_original_range_if_inside_single_mapping(self):
        assert mapped_ranges(Range(0, 5), self.mappings) == [Range(50, 55)]
        assert mapped_ranges(Range(13, 15), self.mappings) == [Range(93, 95)]

    async def test_split_into_two_mappings(self):
        assert mapped_ranges(Range(8, 12), self.mappings) == [
            Range(58, 59),
            Range(90, 92),
        ]

    async def test_non_mapped_values_get_separate_range(self):
        assert mapped_ranges(Range(18, 35), self.mappings) == [
            Range(98, 99),  # Mapping 2
            Range(20, 29),  # No mapping
            Range(1000, 1005),  # Mapping 3
        ]


def test_part1():
    assert part1(TEST_INPUT_PATH) == 35


# @pytest.mark.skip()
def test_part2():
    assert part2(TEST_INPUT_2_PATH) == 46
