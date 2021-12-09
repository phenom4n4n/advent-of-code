import math
from typing import List, Tuple, Dict, Set

from utils import run

Coord = Tuple[int, int]
Line = List[int]
Grid = List[Line]


def convert(line: str) -> Line:
    return [int(x) for x in line]


def find_adjacent(
    data: Grid,
    line: Line,
    x: int,
    y: int,
) -> Dict[Coord, int]:
    adjacent = {}
    if y > 0:
        new_y = y - 1
        height = data[new_y][x]
        adjacent[(x, new_y)] = height
    if x > 0:
        new_x = x - 1
        height = line[new_x]
        adjacent[(new_x, y)] = height
    if y < len(data) - 1:
        new_y = y + 1
        height = data[new_y][x]
        adjacent[(x, new_y)] = height
    if x < len(line) - 1:
        new_x = x + 1
        height = line[new_x]
        adjacent[(new_x, y)] = height
    return adjacent


@run(c=convert)
def part1(data: Grid):
    lowest = []
    for y, line in enumerate(data):
        for x, n in enumerate(line):
            adjacent = find_adjacent(data, line, x, y).values()
            if all(n < a for a in adjacent):
                lowest.append(n)
    return sum(lowest) + len(lowest)


class BasinFinder:
    __slots__ = ("data", "basin", "searched")

    def __init__(self, data: Grid, *, basin: Dict[Coord, int] = None, searched: Set[Coord] = None):
        self.data = data
        self.basin = basin or {}
        self.searched = searched or set()

    def find(self, start: Coord) -> Dict[Coord, int]:
        adjacent = find_adjacent(self.data, self.data[start[1]], *start)
        for coord, height in adjacent.items():
            if coord in self.searched:
                continue
            self.searched.add(coord)
            if height == 9:
                continue
            self.basin[coord] = height
            finder = self.__class__(self.data, basin=self.basin, searched=self.searched)
            self.basin.update(finder.find(coord))
        return self.basin


@run(c=convert)
def part2(data: Grid):
    lowest = []
    for y, line in enumerate(data):
        for x, n in enumerate(line):
            adjacent = find_adjacent(data, line, x, y)
            if all(n < a for a in adjacent.values()):
                lowest.append((x, y))
    basins = {}
    for coord in lowest:
        finder = BasinFinder(data)
        basins[coord] = finder.find(coord)
    top_basins = sorted(list(basins.values()), key=lambda b: len(b.values()), reverse=True)[:3]
    len_basins = [len(b.values()) for b in top_basins]
    return math.prod(len_basins)
