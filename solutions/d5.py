from collections import Counter
from functools import cached_property
from typing import List, Tuple

from utils import read_input


class Line:
    __slots__ = ("endpoints", "_coords")

    def __init__(self, string: str):
        endpoints = string.split(' ->', 1)
        self.endpoints: Tuple[Tuple[int]] = tuple(map(self.parse_coord, endpoints))
        self._coords: List[Tuple[int, int]] = []

    def __repr__(self):
        return f"Line({self.endpoints[0]} -> {self.endpoints[1]})"

    def parse_coord(self, coord: str) -> Tuple[int, int]:
        return tuple(map(int, coord.split(",")))

    def is_straight(self) -> bool:
        end1, end2 = self.endpoints
        return end1[0] == end2[0] or end1[1] == end2[1]

    @property
    def all_coords(self) -> List[Tuple[int, int]]:
        if self._coords:
            return self._coords
        end1, end2 = self.endpoints
        x1, y1 = end1
        x2, y2 = end2
        x_inc = 1 if x1 < x2 else -1
        y_inc = 1 if y1 < y2 else -1
        self._coords.append(end1)
        while x1 != x2 or y1 != y2:
            if x1 != x2:
                x1 += x_inc
            if y1 != y2:
                y1 += y_inc
            self._coords.append((x1, y1))
        return self._coords


class Field:
    def __init__(self, data: List[Line]):
        self.lines = data
        self.end = [0, 0]
        self.grid: Counter = Counter()

    def __repr__(self):
        self.generate_grid()
        lines: List[str] = []
        for y in range(self.end[1] + 1):
            line = [self.grid[(x, y)] for x in range(self.end[0] + 1)]
            lines.append("".join(map(str, line)))
        return "\n".join(lines)

    def generate_grid(self):
        if self.grid:
            return
        for line in self.lines:
            self.end[0] = max(self.end[0], *map(lambda e: e[0], line.endpoints))
            self.end[1] = max(self.end[1], *map(lambda e: e[1], line.endpoints))
            for coord in line.all_coords:
                self.grid[coord] += 1

    @property
    def total_overlaps(self) -> int:
        self.generate_grid()
        return sum(v > 1 for v in self.grid.values())


data = read_input(__file__, c=Line)


def part1():
    field = Field(line for line in data if line.is_straight())
    print(field.total_overlaps)


def part2():
    field = Field(data)
    print(field.total_overlaps)


if __name__ == "__main__":
    part1()
    part2()
