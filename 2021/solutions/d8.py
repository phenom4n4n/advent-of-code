from itertools import permutations
from typing import Dict, List, FrozenSet, Tuple

from utils import run

len_to_num = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}
num_to_seg = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
Key = Dict[FrozenSet[str], int]

test = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


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
    seg_key = {}

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
