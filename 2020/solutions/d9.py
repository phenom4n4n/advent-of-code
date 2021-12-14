from utils import run


def is_valid(preamble: list[int], n: int) -> bool:
    for i in preamble:
        for j in preamble:
            if i != j and i + j == n:
                return True
    return False


@run(c=int)
def part1(data: list[int], *, length: int = 25) -> int:
    for i in range(length, len(data) - 1):
        preamble = data[i - length:i]
        n = data[i]
        if not is_valid(preamble, n):
            return n


def check_contiguous(data: list[int], n: int) -> list[int]:
    total = 0
    used = []
    for i in data:
        total += i
        used.append(i)
        if total == n:
            return used
    return []


@run(c=int)
def part2(data: list[int]) -> int:
    invalid = part1(data)
    for i in range(len(data)):
        after = data[i:]
        if contiguous := check_contiguous(after, invalid):
            return max(contiguous) + min(contiguous)
