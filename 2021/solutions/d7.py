import math
import statistics
from typing import List

from utils import run


@run(",", c=int)
def part1(data: List[int]) -> int:
    median = int(statistics.median(data))
    return sum(abs(x - median) for x in data)


def calc_fuel(fuel: int, dest: int) -> int:
    dist = abs(dest - fuel)
    return dist * (1 + dist) // 2
    # original below
    # return sum(range(1, dist + 1))


@run(",", c=int)
def part2(data: List[int]) -> int:
    avg = statistics.mean(data)
    avgs = (math.ceil(avg), math.floor(avg))
    sums = [sum(calc_fuel(fuel, dest) for fuel in data) for dest in avgs]
    print(sums)
    return min(sums)

    # below is my original solution, but is slow

    # usages = {}
    # for i in range(min(data), max(data) + 1):
    #    usages[i] = sum(calc_fuel(x, i) for x in data)
    # return min(usages.values())
