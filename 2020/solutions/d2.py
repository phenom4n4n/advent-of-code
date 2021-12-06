from utils import read_input

class PWord:
    def __init__(self, info: str):
        policy, self.char, self.password = map(str.strip, info.split(" "))
        self.char = self.char.strip(":")
        self.min, self.max = map(int, policy.split("-"))

    def __repr__(self):
        return f"PWord({self.min}-{self.max} {self.char}: {self.password})"

    def is_valid(self) -> bool:
        count = self.password.count(self.char)
        return count >= self.min and count <= self.max

    def is_valid2(self) -> bool:
        return (self.password[self.min - 1] + self.password[self.max - 1]).count(self.char) == 1


data = read_input(__file__, c=PWord)


def part1():
    print(sum(p.is_valid() for p in data))


def part2():
    print(sum(p.is_valid2() for p in data))


if __name__ == "__main__":
    part1()
    part2()
