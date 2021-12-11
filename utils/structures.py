from __future__	import annotations

from typing import Tuple, List, TypeVar, Optional, Iterator

__all__ = ("Point", "Grid")

P = TypeVar("P", bound="Point")


class Point:
    __slots__ = ("grid", "x", "y", "value")

    def __init__(self, grid: Grid, coords: Tuple[int, int], value: str):
        self.grid = grid
        self.x, self.y = coords
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(({self.x}, {self.y}): {self.value!r})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def left(self) -> Optional[P]:
        if self.x == 0:
            return
        return self.grid[(self.x - 1, self.y)]

    @property
    def right(self) -> Optional[P]:
        if self.x == self.grid.width - 1:
            return
        return self.grid[(self.x + 1, self.y)]

    @property
    def top(self) -> Optional[P]:
        if self.y == 0:
            return
        return self.grid[(self.x, self.y - 1)]

    @property
    def bottom(self) -> Optional[P]:
        if self.y == self.grid.width - 1:
            return
        return self.grid[(self.x, self.y + 1)]

    @property
    def top_left(self) -> Optional[P]:
        if self.x == 0 or self.y == 0:
            return
        return self.grid[(self.x - 1, self.y - 1)]

    @property
    def top_right(self) -> Optional[P]:
        if self.x == self.grid.width - 1 or self.y == 0:
            return
        return self.grid[(self.x + 1, self.y - 1)]

    @property
    def bottom_left(self) -> Optional[P]:
        if self.x == 0 or self.y == self.grid.width - 1:
            return
        return self.grid[(self.x - 1, self.y + 1)]

    @property
    def bottom_right(self) -> Optional[P]:
        if self.x == self.grid.width - 1 or self.y == self.grid.width - 1:
            return
        return self.grid[(self.x + 1, self.y + 1)]

    def get_points(self, names: List[str]) -> List[P]:
        points = []
        for name in names:
            if point := getattr(self, name, None):
                points.append(point)
        return points

    @property
    def diagonal(self) -> List[P]:
        return self.get_points(["top_left", "top_right", "bottom_left", "bottom_right"])

    @property
    def orthogonal(self) -> List[P]:
        return self.get_points(["left", "right", "top", "bottom"])

    @property
    def adjacent(self) -> List[P]:
        return self.diagonal + self.orthogonal


class Grid:
    __slots__ = ("rows",)

    def __init__(self, rows: List[str], point: P = Point):
        self.rows = []
        for y, row in enumerate(rows):
            points = [point(self, (x, y), c) for x, c in enumerate(row)]
            self.rows.append(points)

    def __repr__(self) -> str:
        rows = ["".join(str(p.value) for p in row) for row in self.rows]
        return "\n".join(rows)

    def __getitem__(self, coords: Tuple[int, int]) -> P:
        x, y = coords
        return self.rows[y][x]

    def __iter__(self) -> Iterator[P]:
        for row in self.rows:
            yield from row

    def __len__(self) -> int:
        return self.length * self.width

    @property
    def length(self) -> int:
        return len(self.rows)

    @property
    def width(self) -> int:
        return len(self.rows[0])
