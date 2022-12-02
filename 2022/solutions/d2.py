from typing import List

from utils import run


@run(c=str)
def part1(data: List[str]):
    scores = {"X": 1, "Y": 2, "Z": 3}
    draws = {"X": "A", "Y": "B", "Z": "C"}
    wins = {"X": "C", "Y": "A", "Z": "B"}
    score = 0
    for line in data:
        a, y = line.split()
        score += scores[y]
        if wins[y] == a:
            score += 6
        elif draws[y] == a:
            score += 3
    return score

@run()
def part2(data: List[str]):
    scores = {"X": 0, "Y": 3, "Z": 6}
    n_scores = {"A": 1, "B": 2, "C": 3}
    loss = {"A": "C", "B": "A", "C": "B"}
    wins = {value: key for key, value in loss.items()}
    score = 0
    for line in data:
        a, y = line.split()
        score += scores[y]
        if y == "X":
            chosen = loss[a]
        elif y == "Y":
            chosen = a
        else:
            chosen = wins[a]
        score += n_scores[chosen]
    return score
