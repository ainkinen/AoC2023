import os
import re
from collections import defaultdict
from typing import Any, NamedTuple

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class Wire(NamedTuple):
    from_id: str
    to_id: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Wire):
            return False

        if self.from_id == other.from_id and self.to_id == other.to_id:
            return True

        if self.from_id == other.to_id and self.to_id == other.from_id:
            return True

        return False


def parse_wires(line: str) -> list[Wire]:
    from_id, *to_ids = re.findall("[a-z]+", line)
    return [Wire(from_id, to_id) for to_id in to_ids]


def part1(input_path: str = INPUT_PATH) -> int:
    lines = read_as_lines(input_path)

    graph: dict[str, set[str]] = defaultdict(set)
    for line in lines:
        wires = parse_wires(line)
        for w in wires:
            # Add two both directions as nodes
            graph[w.from_id].add(w.to_id)
            graph[w.to_id].add(w.from_id)

    nodes = set(graph)

    def outside_connections(node: str) -> int:
        return len(graph[node] - nodes)

    while sum(map(outside_connections, nodes)) != 3:
        max_connected_node = max(nodes, key=outside_connections)
        nodes.remove(max_connected_node)

    return len(nodes) * len(set(graph) - nodes)


def part2(input_path: str = INPUT_PATH) -> int:
    return 0
