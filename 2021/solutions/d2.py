from typing import List

from utils import run


@run()
def part1(data: List[str]):
    horizontal = 0
    vertical = 0
    for line in data:
        command, amount = line.split(" ", 1)
        amount = int(amount)
        if command == "up":
            vertical -= amount
        elif command == "down":
            vertical += amount
        elif command == "forward":
            horizontal += amount
    return horizontal * vertical


@run()
def part2(data: List[str]):
    horizontal = 0
    aim = 0
    vertical = 0
    for line in data:
        command, amount = line.split(" ", 1)
        amount = int(amount)
        if command == "up":
            aim -= amount
        elif command == "down":
            aim += amount
        elif command == "forward":
            horizontal += amount
            vertical += (amount * aim)
    return horizontal * vertical
