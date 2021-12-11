from typing import List, Set

from utils import run, Point, Grid


class Octopus(Point):
    def __init__(self, *args):
        super().__init__(*args)
        self.value: int = int(self.value)

    def increase(self):
        self.value += 1
        if self.value > 9 and not self.flashed:
            self.flash()
            return
        return

    def flash(self):
        self.grid.flashed.add(self)
        self.grid.flashes += 1
        for octo in self.adjacent:
            octo.increase()

    @property
    def flashed(self) -> bool:
        return self in self.grid.flashed


class Cavern(Grid):
    __slots__ = ("current_step", "flashes", "flashed")
    def __init__(self, rows: List[str]):
        super().__init__(rows, Octopus)
        self.current_step: int = 0
        self.flashes: int = 0
        self.flashed: Set[Octopus] = set()

    def step(self) -> int:
        flashes = self.flashes
        self.current_step += 1
        for octo in self:
            octo.increase()
        for octo in self.flashed:
            octo.value = 0
        self.flashed = set()
        return self.flashes - flashes


@run()
def part1(data: List[str]) -> int:
    cavern = Cavern(data)
    flashes = 0
    for _ in range(100):
        step_flashes  = cavern.step()
        flashes += step_flashes
    return flashes

@run()
def part2(data: List[str]) -> int:
    cavern = Cavern(data)
    while True:
        step_flashes = cavern.step()
        if step_flashes == len(cavern):
            return cavern.current_step
