from typing import List, Tuple

from utils import run


def fold(coords: List[Tuple[int, int]], i: int, value: int) -> List[Tuple[int, int]]:
    new_coords = set()
    for coord in coords:
        if coord[i] < value:
            new_coords.add(coord)
        elif coord[i] != value:
            new_coord = list(coord)
            n_i = value - abs(value - new_coord[i])
            new_coord[i] = n_i
            new_coords.add(tuple(new_coord))
    return list(new_coords)


@run("\n\n")
def part1(data: List[str]) -> int:
    coords = [tuple(map(int, line.split(",", 1))) for line in data[0].split("\n")]
    fold_instruction = data[1].split("\n", 1)[0].split(" ")[-1]
    axis, value = fold_instruction.split("=", 1)
    value = int(value)
    folded = fold(coords, 0 if axis == "x" else 1, value)
    return len(folded)


def visualize(coords: List[Tuple[int, int]]) -> str:
    x_max, y_max = coords[0]
    for x, y in coords[1:]:
        x_max = max(x_max, x)
        y_max = max(y_max, y)
    row = [" " for x in range(x_max + 1)]
    grid = [row.copy() for y in range(y_max + 1)]
    for coord in coords:
        grid[coord[1]][coord[0]] = "#"
    return "\n".join("".join(row) for row in grid)


@run("\n\n")
def part2(data: List[str]) -> str:
    coords = [tuple(map(int, line.split(",", 1))) for line in data[0].split("\n")]
    for f_i in data[1].split("\n"):
        axis, value = f_i.split(" ")[-1].split("=", 1)
        value = int(value)
        coords = fold(coords, 0 if axis == "x" else 1, value)
    print(visualize(coords))
    return "see answer above"
