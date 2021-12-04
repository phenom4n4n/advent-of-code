from utils import read_input


data = read_input(__file__, "\n\n", c=str)


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
                print("row", row)
                return row
        for column in self.columns:
            if self.check_list(column):
                print("column", column)
                return column
        return False


def part1():
    draws = map(int, data[0].split(","))
    drawn = []
    boards = [Board(d) for d in data[1:]]
    for draw in draws:
        drawn.append(draw)
        for board in boards:
            result = board.mark(draw)
            if result:
                print(drawn)
                total = sum(n for n in board.nums if n not in drawn)
                print(total, total * drawn[-1])
                return


def part2():
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
    print(drawn)
    total = sum(n for n in last_board.nums if n not in drawn)
    print(total, total * drawn[-1])
    return


if __name__ == "__main__":
    part1()
    part2()
