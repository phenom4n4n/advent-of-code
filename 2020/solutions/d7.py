from __future__ import annotations

import re
from typing import List, Dict, Set

from utils import run

CONTAINS_RE = re.compile(r"(\d+) (\w+ \w+)")
test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


class Bag:
    bags: Dict[str, Bag] = {}

    __slots__ = ("color", "contains")

    def __init__(self, color: str, contains: Dict[Bag, int]):
        self.color = color
        self.contains = contains

    def __eq__(self, other):
        return self.color == other.color

    def __hash__(self):
        return hash(self.color)

    def __repr__(self):
        contains = ", ".join(f"{k.color} ({v})" for k, v in self.contains.items())
        return f"Bag({self.color}: {contains})"

    @classmethod
    def create_bag(cls, color: str, contains: Dict[Bag, int]):
        if color in cls.bags:
            bag = cls.bags[color]
            bag.contains.update(contains)
            return bag
        bag = Bag(color, contains)
        cls.bags[color] = bag
        return bag

    @classmethod
    def from_string(cls, line: str):
        color, contained = line.rstrip(".").split(" bags contain ")
        if contained == "no other bags":
            return cls.create_bag(color, {})
        contains = {}
        for bag in contained.split(", "):
            match = CONTAINS_RE.match(bag)
            if not match:
                raise ValueError(f"Cannot parse bag {bag}")
            count, bag_color = match.groups()
            contains[cls.create_bag(bag_color, {})] = int(count)
        return cls.create_bag(color, contains)

    def can_hold(self, color: str) -> bool:
        contains = False
        for bag in self.contains:
            if color == bag.color or bag.can_hold(color):
                contains = True
        return contains

    def must_contain(self) -> int:
        total = 0
        for bag, count in self.contains.items():
            total += count
            total += count * bag.must_contain()
        return total


@run(c=Bag.from_string)
def part1(data: List[Bag]):
    bags = {bag for bag in data if bag.can_hold("shiny gold")}
    return len(bags)


@run(c=Bag.from_string)
def part2(data: List[Bag]):
    bag = Bag.bags["shiny gold"]
    return bag.must_contain()
