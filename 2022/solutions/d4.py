from typing import List, Tuple

from utils import run


@run()
def part1(data: List[str]):
    total = 0
    for line in data:
        sec1, sec2 = line.split(",")
        sec1 = tuple(map(int, sec1.split("-")))
        sec2 = tuple(map(int, sec2.split("-")))
        if sec1[1] - sec1[0] >= sec2[1] - sec2[0]:
            greater = sec1
            lesser = sec2
        else:
            greater = sec2
            lesser = sec1
        if lesser[0] >= greater[0] and lesser[1] <= greater[1]:
            total += 1
    return total


def check_overlap(greater: Tuple[int, int], lesser: Tuple[int, int]):
    if lesser[0] >= greater[0] and lesser[1] <= greater[1]:
        return True
    if lesser[0] >= greater[0] and lesser[0] <= greater[1]:
        return True
    if lesser[1] >= greater[0] and lesser[1] <= greater[1]:
        return True
    return False


@run()
def part2(data: List[str]):
    total = 0
    for line in data:
        sec1, sec2 = line.split(",")
        sec1 = tuple(map(int, sec1.split("-")))
        sec2 = tuple(map(int, sec2.split("-")))
        if sec1[1] - sec1[0] >= sec2[1] - sec2[0]:
            greater = sec1
            lesser = sec2
        else:
            greater = sec2
            lesser = sec1
        if check_overlap(greater, lesser):
            total += 1
    return total
