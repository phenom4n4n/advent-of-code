from __future__	import annotations

import itertools
from typing import Any, Tuple, List, TypeVar, Optional, Iterator, Generic, Iterable

from .input import Converter, T

__all__ = ("Point", "Grid", "LinkedList")

P = TypeVar("P", bound="Point")
N = TypeVar("N")


class Point:
    __slots__ = ("grid", "x", "y", "value")

    def __init__(self, grid: Grid, coords: Tuple[int, int], value: str, *, c: Converter = str):
        self.grid = grid
        self.x, self.y = coords
        self.value: T = c(value)

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

    def __init__(self, rows: List[str], point: P = Point, **kwargs: Any):
        self.rows: list[list[P]] = []
        for y, row in enumerate(rows):
            points = [point(self, (x, y), c, **kwargs) for x, c in enumerate(row)]
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
    def columns(self) -> List[Tuple[P]]:
        return list(zip(*self.rows))

    @property
    def length(self) -> int:
        return len(self.rows)

    @property
    def width(self) -> int:
        return len(self.rows[0])


class LinkedList(Generic[N]):
    __slots__ = ("head", "tail", "length")

    class Node(Generic[N]):
        __slots__ = ("value", "next", "previous")

        def __init__(self, value: N, next: Optional[LinkedList.Node[N]], previous: Optional[LinkedList.Node[N]]):
            self.value = value
            self.next = next
            self.previous = previous

    def __init__(self, iterable: Iterable = None) -> None:
        self.head = None
        self.tail = None
        self.length = 0

        if iterable:
            for value in iterable:
                self.append(value)

    def __iter__(self) -> Iterator[N]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self)!r})"

    def append(self, value: N) -> None:
        node = self.Node(value, None, None)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
            node.previous = self.tail
        self.tail = node
        self.length += 1

    def appendleft(self, value: N) -> None:
        node = self.Node(value, None, None)
        if self.head is None:
            self.tail = node
        else:
            self.head.previous = node
            node.next = self.head
        self.head = node
        self.length += 1

    def pop(self) -> N:
        if self.tail is None:
            raise IndexError("pop from empty list")
        value = self.tail.value
        self.tail = self.tail.previous
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self.length -= 1
        return value

    def popleft(self) -> N:
        if self.head is None:
            raise IndexError("pop from empty list")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.previous = None
        self.length -= 1
        return value

    def extend(self, iterable: Iterable[N]) -> None:
        if isinstance(iterable, LinkedList):
            if iterable.head is None:
                return
            if self.head is None:
                self.head = iterable.head
            else:
                self.tail.next = iterable.head
                iterable.head.previous = self.tail
            self.tail = iterable.tail
            self.length += iterable.length
        else:
            for value in iterable:
                self.append(value)

    def extendleft(self, iterable: Iterable[N]) -> None:
        if isinstance(iterable, LinkedList):
            if iterable.head is None:
                return
            if self.head is None:
                self.tail = iterable.tail
            else:
                self.head.previous = iterable.tail
                iterable.tail.next = self.head
            self.head = iterable.head
            self.length += iterable.length
        else:
            for value in iterable:
                self.appendleft(value)

    def cut(self, length: int) -> LinkedList:
        new_list = LinkedList()
        if length == 0:
            return new_list
        for _ in range(length):
            new_list.append(self.popleft())
        return new_list

    def copy(self, length: Optional[int] = None):
        if length is not None:
            return LinkedList(itertools.islice(self, length))
        new_list = LinkedList()
        for value in self:
            new_list.append(value)
        return new_list
    