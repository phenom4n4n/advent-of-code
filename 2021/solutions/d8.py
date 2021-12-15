from typing import Dict, List, FrozenSet

from utils import run

len_to_num = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}
Key = Dict[FrozenSet[str], int]


@run("\n")
def part1(data: List[str]) -> int:
    total = 0
    for line in data:
        _, o = line.split(" | ", 2)
        for n in o.split():
            if len_to_num.get(len(n)):
                total += 1
    return total


def decode_line(line: str) -> Key:
    i, _ = line.split(" | ", 2)
    key = {}
    reverse_key = {}

    for sig in i.split():
        if n := len_to_num.get(len(sig)):
            frozen = frozenset(sig)
            key[frozen] = n
            reverse_key[n] = frozen

    for sig in i.split():
        frozen = frozenset(sig)
        if frozen in key:
            continue
        if len(sig) == 5:
            if frozen.issuperset(reverse_key[1]):
                key[frozen] = 3
            elif len(frozen.intersection(reverse_key[4])) == 3:
                key[frozen] = 5
            else:
                key[frozen] = 2
        elif len(sig) == 6:
            if frozen.issuperset(reverse_key[4]):
                key[frozen] = 9
            elif frozen.issuperset(reverse_key[1]):
                key[frozen] = 0
            else:
                key[frozen] = 6
    return key


@run("\n")
def part2(data: List[str]) -> int:
    total = []
    for line in data:
        key = decode_line(line)
        _, o = line.split(" | ", 2)
        nums = []
        for sig in o.split():
            num = str(key.get(frozenset(sig)))
            nums.append(num)
        final = int("".join(nums))
        total.append(final)
    return sum(total)
