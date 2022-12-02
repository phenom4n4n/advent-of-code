from utils import Grid, run, Point


test = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def find_path(grid: Grid, point: Point) -> int:
    next_p = min(point.get_points(("bottom", "right")), key=lambda p: p.value)
    print(next_p)
    if next_p == grid[-1, -1]:
        return point.value
    return point.value + find_path(grid, next_p)


@run(override=test)
def part1(data: list[str]):
    grid = Grid(data, c=int)
    start = grid[0, 0]
    return find_path(grid, start)
