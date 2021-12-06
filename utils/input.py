from datetime import datetime, timezone, timedelta
import os
from pathlib import Path
from typing import Callable, List, Optional, Tuple, TypeVar, Union

__all__ = ("get_date", "read_input", "fetch_input", "PROJECT_ROOT")

T = TypeVar("T")
Converter = Callable[[str], T]

PROJECT_ROOT = Path(__file__).parent.parent


def get_date(day: Union[int, str] = None, year: int = None) -> datetime:
    tz = timezone(timedelta(hours=-5))
    if isinstance(day, str):
        # if it's a string, it should be the file's name
        path = Path(day).resolve()
        day = int(path.stem.lstrip("d"))
        year = int(path.parent.parent.stem)
    else:
        now = datetime.now(tz)
        # assumes the file is from the current day in EST
        if day is None:
            day = now.day
        if year is None:
            year = now.year
    if day < 1 or day > 25:
        raise ValueError(f"day must be between 1 and 25, not {day}")
    return datetime(year, 12, day, tzinfo=tz)


def _return_input(data: str, splitter: str, c: Callable[[str], T]) -> List[T]:
    return [c(l) for l in data.strip().split(splitter)]


def read_input(
    day: Union[int, str] = None,
    splitter: str = "\n",
    *,
    c: Converter = str,
    override: str = None,
    year: int = 2021,
) -> List[T]:
    if override:
        return _return_input(override, splitter, c)
    date = get_date(day, year)
    path = PROJECT_ROOT / str(date.year) / "input" / f"d{date.day}.txt"
    try:
        path.resolve(strict=True)
    except FileNotFoundError:
        data = fetch_input(date.day, date.year)
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
    return _return_input(data, splitter, c)


def _check_cookie(cookie: Optional[str]) -> bool:
    return cookie is not None and cookie != "None"


# the imports in this function aren't top-level imported to save time when they aren't needed
def fetch_input(day: Union[int, str, datetime] = None, year: int = 2021) -> List[str]:
    date = get_date(day, year) if not isinstance(day, datetime) else day
    session_cookie = os.getenv("AOC_SESSION")
    if not _check_cookie(session_cookie):
        from dotenv import load_dotenv

        load_dotenv()
        session_cookie = os.getenv("AOC_SESSION")
    if not _check_cookie(session_cookie):
        raise ValueError("set your session cookie in the .env file")

    import requests

    url = f"https://adventofcode.com/{date.year}/day/{date.day}/input"
    r = requests.get(url, cookies={"session": session_cookie})
    if r.status_code < 200 or r.status_code >= 300:
        raise RuntimeError(f"({r.status_code}) An HTTP error occurred for {url!r}:\n{r.text}")
    return r.text
