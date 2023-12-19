import operator
import os
import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Iterable

from aoc2023.utils.files import read_as_string

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclass
class Rule:
    field: str
    op: Callable[[int, int], bool]
    comparison: int
    destination: str


@dataclass
class Workflow:
    rules: list[Rule]
    default_dest: str

    def get_dest(self, part: Part) -> str:
        for rule in self.rules:
            if rule.op(getattr(part, rule.field), rule.comparison):
                return rule.destination

        return self.default_dest


def parse_rule(rule_str: str) -> Rule:
    rule_p = r"(\w+)([<>])(\d+):(\w+)"
    match = re.match(rule_p, rule_str)
    if not match:
        raise Exception(f"Invalid rule str {rule_str}")

    groups = match.groups()
    return Rule(
        field=groups[0],
        op=operator.lt if groups[1] == "<" else operator.gt,
        comparison=int(groups[2]),
        destination=groups[3],
    )


def parse_workflows(workflow_section: str) -> dict[str, Workflow]:
    workflows: dict[str, Workflow] = {}
    for line in workflow_section.split("\n"):
        name, rest = line.split("{")

        *rule_strs, rest = rest.split(",")
        default = rest[:-1]
        workflows[name] = Workflow(
            rules=[parse_rule(s) for s in rule_strs],
            default_dest=default,
        )

    return workflows


def parse_parts(parts_section: str) -> list[Part]:
    p = r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"

    parts: list[Part] = []
    for line in parts_section.split("\n"):
        match = re.match(p, line)
        if not match:
            raise Exception(f"Invalid part str {line}")
        new_part = Part(*[int(g) for g in match.groups()])
        parts.append(new_part)

    return parts


def part1(input_path: str = INPUT_PATH) -> int:
    sections = [s.strip() for s in read_as_string(input_path).split("\n\n")]

    workflows = parse_workflows(sections[0])
    parts = parse_parts(sections[1])

    accepted = []
    rejected = []
    for part in parts:
        flow = "in"
        while flow not in "AR":
            flow = workflows[flow].get_dest(part)

        if flow == "A":
            accepted.append(part)
        else:
            rejected.append(part)

    return sum([p.x + p.m + p.a + p.s for p in accepted])


Range = tuple[int, int]


@dataclass
class Section:
    x: Range
    m: Range
    a: Range
    s: Range

    def size(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )


def split_flows(
    input_section: Section, workflow: Workflow
) -> Iterable[tuple[str, Section]]:
    # -> new_id, section
    section = input_section
    for rule in workflow.rules:
        rule_field_range = getattr(section, rule.field)
        # Check if the section is cut by the comparison, yield splits
        if rule_field_range[0] < rule.comparison < rule_field_range[1]:
            if rule.op == operator.lt:
                out_flow = deepcopy(section)
                setattr(
                    out_flow, rule.field, (rule_field_range[0], rule.comparison - 1)
                )
                yield rule.destination, out_flow
                setattr(section, rule.field, (rule.comparison, rule_field_range[1]))
            elif rule.op == operator.gt:
                out_flow = deepcopy(section)
                setattr(
                    out_flow, rule.field, (rule.comparison + 1, rule_field_range[1])
                )
                yield rule.destination, out_flow
                setattr(section, rule.field, (rule_field_range[0], rule.comparison))

    yield workflow.default_dest, section


def part2(input_path: str = INPUT_PATH) -> int:
    sections = [s.strip() for s in read_as_string(input_path).split("\n\n")]

    workflows = parse_workflows(sections[0])

    flow_dict: dict[str, list[Section]] = {
        "in": [Section((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    }

    # Process until all ranges converge to A or R
    while any(key not in "AR" for key in flow_dict.keys()):
        new_ranges: dict[str, list[Section]] = defaultdict(list)
        for key, ranges in flow_dict.items():
            # Done ranges passed as-is
            if key in "AR":
                new_ranges[key] += ranges
                continue

            # Generate output flows for all inputs
            for in_flow in flow_dict[key]:
                for out_id, out_flow in split_flows(in_flow, workflows[key]):
                    new_ranges[out_id].append(out_flow)

        flow_dict = new_ranges

    # Sum of sizes of all accepted ranges
    return sum([flow.size() for flow in flow_dict["A"]])
