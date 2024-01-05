import os
import re
from fractions import Fraction
from itertools import combinations
from typing import NamedTuple

import sympy as sp
from sympy.core.relational import Relational

from aoc2023.utils.files import read_as_lines

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class Hail(NamedTuple):
    px: int
    py: int
    pz: int
    dx: int
    dy: int
    dz: int


def parse_hails(line: str) -> Hail:
    numbers = re.findall(r"(-?\d+)", line)

    return Hail(*map(int, numbers))


def check_2d_intersect(a: Hail, b: Hail) -> tuple[Fraction, Fraction] | None:
    """
    X location
    a.px + t_a * a.dx = b.px + t_b * b.dx
    -> a.px + t_a * a.dx - b.px - t_b * b.dx = 0

    Y location
    a.py + t_a * a.dy = b.py + t_b * b.dy
    -> a.py + t_a * a.dy - b.py - t_b * b.dy = 0
    """

    unknowns = sp.symbols("t_a t_b", positive=True)
    t_a, t_b = unknowns
    eqs = [
        a.px + t_a * a.dx - b.px - t_b * b.dx,
        a.py + t_a * a.dy - b.py - t_b * b.dy,
    ]
    solution = sp.solve(eqs, [t_a, t_b])

    if not solution:
        return None

    x = a.px + solution[t_a] * a.dx
    y = a.py + solution[t_a] * a.dy

    return x, y


def part1(
    input_path: str = INPUT_PATH,
    area_min: int = 200_000_000_000_000,
    area_max: int = 400_000_000_000_000,
) -> int:
    hails = [parse_hails(line) for line in read_as_lines(input_path)]
    combos = list(combinations(hails[:300], 2))
    maybe_intersections = [check_2d_intersect(a, b) for a, b in combos]
    intersections = filter(None, maybe_intersections)

    in_range = filter(
        lambda i: area_min <= i[0] <= area_max and area_min <= i[1] <= area_max,
        intersections,
    )

    return len(list(in_range))


def part2(input_path: str = INPUT_PATH) -> int:
    """
    Throw should intersect with all hails

    For all axes & all hails:
    x + t_n * dx = hail_n.px * t_n * hail_n.dx

    Nine variables = 3 hails * 3 axes per hail
    """
    first_three_hails = [parse_hails(line) for line in read_as_lines(input_path)][:3]

    unknowns = sp.symbols("x y z dx dy dz t1 t2 t3")
    x, y, z, dx, dy, dz, t1, t2, t3 = unknowns
    eqs: list[Relational] = []

    for t, h in zip([t1, t2, t3], first_three_hails):
        eqs.append(sp.Eq(x + t * dx, h.px + t * h.dx))
        eqs.append(sp.Eq(y + t * dy, h.py + t * h.dy))
        eqs.append(sp.Eq(z + t * dz, h.pz + t * h.dz))

    solution = sp.solve(eqs, unknowns, dict=True)[0]

    return solution[x] + solution[y] + solution[z]
