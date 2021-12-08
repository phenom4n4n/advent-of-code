import re
from typing import List

from utils import run


HEIGHT_RE = re.compile(r"^(\d+)(cm|in)$")
HCL_RE = re.compile(r"^#[0-9a-f]{6}$")
PID_RE = re.compile(r"^\d{9}$")


def _height_check(entry: str) -> bool:
    match = HEIGHT_RE.match(entry)
    if not match:
        return False
    height = int(match.group(1))
    unit = match.group(2)
    if unit == "cm":
        return 150 <= height <= 193
    elif unit == "in":
        return 59 <= height <= 76


fields = {
    "byr": lambda x: int(x) <= 2002 and int(x) >= 1920,
    "iyr": lambda x: int(x) <= 2020 and int(x) >= 2010,
    "eyr": lambda x: int(x) <= 2030 and int(x) >= 2020,
    "hgt": _height_check,
    "hcl": lambda x: HCL_RE.match(x) is not None,
    "ecl": lambda x: x in "amb blu brn gry grn hzl oth".split(),
    "pid": lambda x: PID_RE.match(x) is not None,
}


def _should_add(pp: str) -> bool:
    return all(field in pp for field in fields)


@run("\n\n")
def part1(data: List[str]):
    return sum(_should_add(pp) for pp in data)


def _validate_passport(pp: str) -> bool:
    if not _should_add(pp):
        return False
    for f in pp.split():
        field, value = f.split(":")
        if field == "cid":
            continue
        if not fields[field](value):
            return False
    return True


@run("\n\n")
def part2(data: List[str]):
    return sum(_validate_passport(pp) for pp in data)
