from utils import run


class Instruction:
    __slots__ = ("line", "opp", "arg", "uses")

    def __init__(self, line: str):
        self.line = line
        self.opp, self.arg = line.split(" ", 1)
        self.arg = int(self.arg)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.opp} {self.arg})"


class RepeatError(Exception):
    def __init__(self, instr: Instruction, acc: int):
        self.acc = acc
        super().__init__(f"{instr.line} was attempted to be repeated. Accumulator: {acc}")


class Accumulator:
    __slots__ = ("instructions", "acc", "index", "executed")

    def __init__(self, instructions: list[Instruction]):
        self.instructions = instructions
        self.acc = 0
        self.index = 0
        self.executed: set[int] = set()

    def run(self):
        i = self.index
        instr = self.instructions[i]
        if i in self.executed:
            raise RepeatError(instr, self.acc)
        match instr.opp:
            case "acc":
                self.acc += instr.arg
                self.index += 1
            case "jmp":
                self.index += instr.arg
            case "nop":
                self.index += 1
        self.executed.add(i)
        return self.run()


@run(c=Instruction)
def part1(data: list[Instruction]) -> int:
    accumulator = Accumulator(data)
    try:
        accumulator.run()
    except RepeatError as e:
        return e.acc


@run(c=Instruction)
def part2(data: list[Instruction]) -> int:
    for line in data:
        original = line.opp
        if line.opp == "acc":
            continue
        line.opp = {"nop": "jmp", "jmp": "nop"}[line.opp]
        accumulator = Accumulator(data)
        try:
            accumulator.run()
        except RepeatError:
            line.opp = original
        except IndexError:
            return accumulator.acc
