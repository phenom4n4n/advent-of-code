import re

from utils import run, LinkedList

INSTRUCTION_RE = re.compile(r"move (\d+) from (\d+) to (\d+)")


def read_crates(crates: str) -> dict[int, LinkedList[str]]:
    crates = crates.splitlines()
    stacks = {int(n): LinkedList[str]() for n in crates[-1].split()}
    for level in crates[:-1]:
        read_level(level, stacks)
    return stacks


def read_level(level: str, stacks: dict[int, LinkedList[str]]) -> str:
    end = len(stacks) + 1
    for i in range(1, end):
        value = level[:3]
        if value != "   ":
            stacks[i].append(value.strip("[]"))
        if i != end - 1:
            level = level[4:]


@run("\n\n")
def part1(data: list[str]) -> int:
    crates, instructions = data
    stacks = read_crates(crates)
    for instruction in instructions.splitlines():
        match = INSTRUCTION_RE.match(instruction)
        count, from_stack, to_stack = map(int, match.groups())
        moving = stacks[from_stack].cut(count)
        for crate in moving:
            stacks[to_stack].appendleft(crate)
    return "".join(s.head.value for s in stacks.values())


@run("\n\n")
def part2(data: list[str]) -> int:
    crates, instructions = data
    stacks = read_crates(crates)
    for instruction in instructions.splitlines():
        match = INSTRUCTION_RE.match(instruction)
        count, from_stack, to_stack = map(int, match.groups())
        moving = stacks[from_stack].cut(count)
        stacks[to_stack].extendleft(moving)
    return "".join(s.head.value for s in stacks.values())
