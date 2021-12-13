from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple, DefaultDict, Set, Dict

from utils import run


def convert(line: str) -> Tuple[Node, Node]:
    return tuple(map(Node.create_node, line.split("-", 1)))


class Node:
    __slots__ = ("name", "small", "finder")
    NODES: Dict[str, Node] = {}

    def __init__(self, name: str):
        self.name = name
        self.small = name.islower()

    def __repr__(self):
        return f"Node({self.name})"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def create_node(cls, name: str) -> Node:
        if name in cls.NODES:
            return cls.NODES[name]
        node = cls(name)
        cls.NODES[name] = node
        return node

    @property
    def start_or_end(self) -> bool:
        return self.name in {"start", "end"}


class PathFinder:
    __slots__ = ("adjacency", "nodes", "paths", "allow_double")

    def __init__(self, data: List[Tuple[str, str]], allow_double: bool = False):
        self.adjacency: DefaultDict[Node, List[Node]] = defaultdict(list)
        self.nodes: Dict[str, Node] = {}
        for a, b in data:
            self.adjacency[a].append(b)
            self.adjacency[b].append(a)
        self.allow_double = allow_double
        self.paths: int = 0

    @property
    def start(self) -> Node:
        return Node.NODES["start"]

    @property
    def end(self) -> Node:
        return Node.NODES["end"]

    def search(self, start: Node, visited: Set[Node], revisit: bool = True) -> int:
        if start == self.end:
            self.paths += 1
            return
        for node in self.adjacency[start]:
            if self.allow_double and node.small and node in visited:
                if not revisit or node.start_or_end:
                    continue
                self.search(node, {*visited, start}, False)
            elif self.allow_double or not node.small or node not in visited:
                self.search(node, {*visited, start}, revisit)
        return self.paths


@run(c=convert)
def part1(data: List[Tuple[Node, Node]]) -> int:
    finder = PathFinder(data)
    return finder.search(finder.start, set())


@run(c=convert)
def part2(data: List[Tuple[Node, Node]]) -> int:
    finder = PathFinder(data, True)
    return finder.search(finder.start, set())
