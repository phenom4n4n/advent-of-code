from collections import defaultdict
from typing import List

from utils import read_input


def convert(line: str) -> List[int]:
    return [int(x) for x in line]


data = read_input(__file__, c=convert)


def part1():
    common = defaultdict(int)
    for line in data:
        for i, bit in enumerate(line):
            common[i] += bit
    gamma_bits = ""
    epsilon_bits = ""
    for value in common.values():
        common_bit = len(data) / value >= 2
        gamma_bits += str(int(common_bit))
        epsilon_bits += str(int(not common_bit))
    gamma = int(gamma_bits, 2)
    epsilon = int(epsilon_bits, 2)
    print(gamma, epsilon, gamma * epsilon)


def _get_common_bit_lines(lines: List[int], index: int = 0, least: bool = False) -> int:
    common = sum(line[index] for line in lines)
    common_bit = len(lines) / common
    if common_bit == 2:
        common_bit = int(not least)
    else:
        common_bit = common_bit > 2
        common_bit = int(common_bit if least else not common_bit)
    common_lines = [n for n in lines if n[index] == common_bit]
    if len(common_lines) == 1:
        return int("".join(map(str, common_lines[0])), 2)
    return _get_common_bit_lines(common_lines, index + 1, least)


def part2():
    o_gen = _get_common_bit_lines(data)
    scrubber = _get_common_bit_lines(data, least=True)
    print(o_gen, scrubber, o_gen * scrubber)


if __name__ == "__main__":
    part1()
    part2()
