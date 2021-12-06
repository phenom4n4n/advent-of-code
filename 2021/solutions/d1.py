from typing import List

from utils import run


@run(c=int)
def part1(data: List[int]):
    increases = 0
    previous = data[0]
    for num in data[1:]:
        if num > previous:
            increases += 1
        previous = num
    return increases


@run(c=int)
def part2(data: List[int]):
    increases = 0
    previous = sum(data[:3])
    for i in range(1, len(data)):
        total = sum(data[i:i+3])
        if total > previous:
            increases += 1
        previous = total
    return increases
