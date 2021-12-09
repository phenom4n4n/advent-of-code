import statistics
from typing import List, Tuple

from utils import run


ROWS = 128
COLUMNS = 8
test = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""


def parse_id(line: str) -> List[int]:
    row_id, column_id = line[:7], line[7:]
    row_id = row_id.replace("F", "0").replace("B", "1")
    row = int(row_id, 2)
    column_id = column_id.replace("L", "0").replace("R", "1")
    column = int(column_id, 2)
    return [row, column, row * 8 + column]


@run(c=parse_id)
def part1(data: List[List[int]]) -> int:
    return max(d[-1] for d in data)


def get_adjacent(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    row, column = coord
    adj = []
    if row > 0:
        if column == 0:
            left = (row - 1, COLUMNS - 1)
        else:
            left = (row - 1, column - 1)
        adj.append(left)
    if row < ROWS - 1:
        if column == COLUMNS - 1:
            right = (row + 1, 0)
        else:
            right = (row + 1, column + 1)
        adj.append(right)
    return adj


@run(c=parse_id)
def part2(data: List[List[int]]) -> int:
    missing = []
    data.sort()
    ids = {(d[0], d[1]): d[-1] for d in data}
    for row in range(ROWS):
        for column in range(COLUMNS):
            if (row, column) not in ids:
                missing.append((row, column))
    for r, c in missing:
        adj = get_adjacent((r, c))
        if all(a in ids for a in adj):
            return r * 8 + c
