import math
from typing import List

from utils import run


class Line:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def __getitem__(self, index: int) -> str:
        return self.pattern[index % len(self.pattern)]


@run(c=Line)
def part1(data: List[Line]):
    trees = 0
    x = 0
    for line in data:
        if line[x] == "#":
            trees += 1
        x += 3
    return trees


def traverse(data: List[Line], r: int, d: int) -> int:
    trees = 0
    x = 0
    for y in range(0, len(data), d):
        if data[y][x] == "#":
            trees += 1
        x += r
    return trees


@run(c=Line)
def part2(data: List[Line]):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    trees = [traverse(data, *slope) for slope in slopes]
    return math.prod(trees)
