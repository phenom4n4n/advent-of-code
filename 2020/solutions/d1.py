from typing import List

from utils import run


@run(c=int)
def part1(data: List[int]):
    for i, n in enumerate(data):
        for k, e in enumerate(data):
            if i == k:
                continue
            if n + e == 2020:
                return n * e


@run(c=int)
def part2(data: List[int]):
    for i, n in enumerate(data):
        for k, e in enumerate(data):
            for j, f in enumerate(data):
                if i == k or k == j or i == j:
                    continue
                if n + e + f == 2020:
                    return n * e * f
