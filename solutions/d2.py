from utils import read_input

data = read_input(__file__, c=str.strip)


def part1():
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
    print(horizontal, vertical, horizontal * vertical)


def part2():
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
    print(horizontal, vertical, aim, horizontal * vertical)


part1()
part2()
