from collections import Counter

from utils import run


def step(template: Counter[str], rules: dict[str, str]) -> str:
    new_template = Counter()
    for k, v in template.items():
        element = rules[k]
        new_template[k[0] + element] += v
        new_template[element + k[1]] += v
    return new_template


def main(data: list[str], iterations: int):
    rules: dict[str, str] = {}
    for rule in data[1].split("\n"):
        k, v = rule.split(" -> ")
        rules[k] = v

    template = data[0]
    counter = Counter()
    for i in range(len(template) - 1):
        counter[template[i:i + 2]] += 1

    for _ in range(iterations):
        counter = step(counter, rules)

    score = Counter(template[0])
    for k, v in counter.items():
        score[k[1]] += v
    common = score.most_common()
    return common[0][1] - common[-1][1]


@run("\n\n")
def part1(data: list[str]) -> int:
    return main(data, 10)


@run("\n\n")
def part2(data: list[str]) -> int:
    return main(data, 40)
