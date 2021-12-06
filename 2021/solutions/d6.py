from collections import Counter
from typing import List

from utils import run


def _get_children(data: List[int], days: int):
    counter = Counter(data)
    for _ in range(days):
        counter = Counter({k - 1: v for k, v in counter.items()})
        counter[6] += counter[-1]
        counter[8] += counter[-1]
        del counter[-1]
    return sum(counter.values())


@run(",", c=int)
def part1(data: List[int]):
    return _get_children(data, 18)


@run(",", c=int)
def part2(data: List[int]):
    return _get_children(data, 256)
