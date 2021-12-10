from collections import Counter
from typing import List

from utils import run


@run("\n\n")
def part1(data: List[str]) -> int:
    total = 0
    for group in data:
        answers = set()
        people = group.split()
        for person in people:
            for answer in person:
                answers.add(answer)
        total += len(answers)
    return total


@run("\n\n")
def part2(data: List[str]) -> int:
    total = 0
    for group in data:
        answers = Counter()
        people = group.split()
        for person in people:
            for answer in person:
                answers[answer] += 1
        total += len(list(filter(lambda x: x == len(people), answers.values())))
    return total
