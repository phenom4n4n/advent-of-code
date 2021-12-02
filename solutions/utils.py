from pathlib import Path
from typing import Callable, List, TypeVar
from datetime import datetime, timezone, timedelta

__all__ = ("read_input",)

T = TypeVar('T')


def read_input(
    day: int = None,
    splitter: str = "\n",
    *,
    c: Callable[[str], T] = str
) -> List[T]:
    if not day:
        day = datetime.now(timezone(timedelta(hours=-5))).day 
        # assumes the file is from the current day in EST
    path = Path(__file__).resolve().parent.parent / "input" / f"d{day}.txt"
    with open(path, "r", encoding="utf-8") as f:
        return [c(l) for l in f.read().strip().split(splitter)]
