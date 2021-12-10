from collections import defaultdict
import statistics
from typing import List

from utils import run

valid_identifiers = {"(": ")", "[": "]", "{": "}", "<": ">"}
reverse_identifiers = {v: k for k, v in valid_identifiers.items()}
invalid_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
valid_scores = {")": 1, "]": 2, "}": 3, ">": 4}


class CorruptedChunkError(Exception):
    def __init__(self, char: str, expected: str):
        self.char = char
        super().__init__(f"Corrupted chunk, expected: {expected}, got: {char}")


def parse_chunks(line: str) -> List[str]:
    chunk_opens = []
    for c in line:
        if c in valid_identifiers:
            chunk_opens.append(c)
        elif (expected := chunk_opens.pop()) != reverse_identifiers[c]:
            raise CorruptedChunkError(c, expected)
    return [valid_identifiers[c] for c in reversed(chunk_opens)]


@run()
def part1(data: List[str]) -> int:
    invalid = []
    for line in data:
        try:
            parse_chunks(line)
        except CorruptedChunkError as e:
            invalid.append(invalid_scores[e.char])
    return sum(invalid)


@run()
def part2(data: List[str]) -> int:
    scores = []
    for line in data:
        try:
            missing = parse_chunks(line)
        except CorruptedChunkError:
            continue
        score = 0
        for m in missing:
            score *= 5
            score += valid_scores[m]
        scores.append(score)
    return statistics.median(scores)
