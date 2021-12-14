from typing import List, Set

from utils import run

test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


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

    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.acc = 0
        self.index = 0
        self.executed: Set[int] = set()

    def run(self):
        i = self.index
        instr = self.instructions[i]
        if i in self.executed:
            raise RepeatError(instr, self.acc)
        if instr.opp == "acc":
            self.acc += instr.arg
            self.index += 1
        elif instr.opp == "jmp":
            self.index += instr.arg
        elif instr.opp == "nop":
            self.index += 1
        self.executed.add(i)
        return self.run()


@run(c=Instruction)
def part1(data: List[Instruction]) -> int:
    accumulator = Accumulator(data)
    try:
        accumulator.run()
    except RepeatError as e:
        return e.acc


@run(c=Instruction)
def part2(data: List[Instruction]) -> int:
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
