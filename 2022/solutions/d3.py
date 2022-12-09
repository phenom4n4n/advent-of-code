import itertools
from typing import List

from utils import run


def find_priority(c: str):
    if c.isupper():
        return ord(c) - ord("A") + 27
    return ord(c) - ord("a") + 1


def chunks(iterable, size):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it,size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it,size))


@run()
def part1(data: List[str]):
    total = 0
    for line in data:
        half = int(len(line) / 2)
        first = line[:half]
        second = line[half:]
        for c in first:
            if c in second:
                total += find_priority(c)
                break
    return total

@run()
def part2(data: List[str]):
    total = 0
    for lines in chunks(data, 3):
        c = set(lines[0]).intersection(lines[1]).intersection(lines[2]).pop()
        total += find_priority(c)
    return total
