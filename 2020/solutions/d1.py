from utils import read_input

data = read_input(__file__, c=int)


def part1():
    for i, n in enumerate(data):
        for k, e in enumerate(data):
            if i == k:
                continue
            if n + e == 2020:
                print(n * e)
                return


def part2():
    for i, n in enumerate(data):
        for k, e in enumerate(data):
            for j, f in enumerate(data):
                if i == k or k == j or i == j:
                    continue
                if n + e + f == 2020:
                    print(n * e * f)
                    return


if __name__ == "__main__":
    part1()
    part2()
