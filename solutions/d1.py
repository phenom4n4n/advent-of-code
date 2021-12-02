from utils import read_input

data = read_input(1, c=int)

def part1():
    increases = 0
    previous = data[0]
    for num in data[1:]:
        if num > previous:
            increases += 1
        previous = num
    print(increases)

def part2():
    increases = 0
    previous = sum(data[:3])
    for i in range(1, len(data)):
        total = sum(data[i:i+3])
        if total > previous:
            increases += 1
        previous = total
    print(increases)

part1()
part2()
