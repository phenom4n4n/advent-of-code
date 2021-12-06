from typing import List

from utils import run


class Board:
    def __init__(self, board: str):
        self.rows = []
        for row in board.split("\n"):
            self.rows.append(list(map(int, row.split())))
        self.columns = zip(*self.rows)
        self.nums = set()
        for row in self.rows:
            self.nums.update(row)
        self.marked = set()

    def mark(self, num: int):
        if num in self.nums:
            self.marked.add(num)
            return self.check()

    def check_list(self, nums):
        for num in nums:
            if num not in self.marked:
                return
        return nums

    def check(self):
        for row in self.rows:
            if self.check_list(row):
                return row
        for column in self.columns:
            if self.check_list(column):
                return column
        return False


@run("\n\n")
def part1(data: List[str]):
    draws = map(int, data[0].split(","))
    drawn = []
    boards = [Board(d) for d in data[1:]]
    for draw in draws:
        drawn.append(draw)
        for board in boards:
            result = board.mark(draw)
            if result:
                total = sum(n for n in board.nums if n not in drawn)
                return total * drawn[-1]


@run("\n\n")
def part2(data: List[str]):
    draws = map(int, data[0].split(","))
    drawn = []
    boards = [Board(d) for d in data[1:]]
    completed = []
    for draw in draws:
        drawn.append(draw)
        for board in boards.copy():
            result = board.mark(draw)
            if result:
                completed.append(board)
                boards.remove(board)
        if not boards:
            break
    last_board = completed[-1]
    total = sum(n for n in last_board.nums if n not in drawn)
    return total * drawn[-1]
