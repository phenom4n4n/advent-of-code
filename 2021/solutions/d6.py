from collections import Counter

from utils import read_input

data = read_input(__file__, ",", c=int)


def _get_children(days: int):
    counter = Counter(data)
    for _ in range(days):
        counter = Counter({k - 1: v for k, v in counter.items()})
        counter[6] += counter[-1]
        counter[8] += counter[-1]
        del counter[-1]
    return sum(counter.values())


def part1():
    print(_get_children(18))


def part2():
    print(_get_children(256))


if __name__ == "__main__":
    part1()
    part2()
