from typing import List

from utils import run


@run("\n\n", c=lambda x: sum(map(int, x.splitlines())))
def part1(data: List[int]):
    return max(data)

@run("\n\n", c=lambda x: sum(map(int, x.splitlines())))
def part2(data: List[int]):
    return sum(sorted(data, reverse=True)[:3])
