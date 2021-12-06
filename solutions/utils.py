from datetime import datetime, timezone, timedelta
import os
from pathlib import Path
from typing import Callable, List, Optional, TypeVar, Union

__all__ = ("get_day", "read_input", "fetch_input")

T = TypeVar('T')

PROJECT_ROOT = Path(__file__).parent.parent


def get_day(day: Union[int, str] = None) -> int:
    if day is None:
        day = datetime.now(timezone(timedelta(hours=-5))).day
        # assumes the file is from the current day in EST
    if isinstance(day, str):
        # if it's a string, it should be the file's name
        day = int(Path(day).resolve().stem.lstrip("d"))
    if day < 1 or day > 25:
        raise ValueError(f"day must be between 1 and 25, not {day}")
    return day


def _return_input(data: str, splitter: str, c: Callable[[str], T]) -> List[T]:
    return [c(l) for l in data.strip().split(splitter)]


def read_input(
    day: Union[int, str] = None,
    splitter: str = "\n",
    *,
    c: Callable[[str], T] = str,
    override: str = None,
) -> List[T]:
    if override:
        return _return_input(override, splitter, c)
    day = get_day(day)
    path = PROJECT_ROOT / "input" / f"d{day}.txt"
    try:
        path.resolve(strict=True)
    except FileNotFoundError:
        data = fetch_input(day)
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
    return _return_input(data, splitter, c)


def _check_cookie(cookie: Optional[str]) -> bool:
    return cookie is not None and cookie != "None"


# the imports in this function aren't top-level imported to save time when they aren't needed
def fetch_input(day: Union[int, str] = None, year: int = 2021) -> List[str]:
    day = get_day(day)

    session_cookie = os.getenv("AOC_SESSION")
    if not _check_cookie(session_cookie):
        from dotenv import load_dotenv

        load_dotenv()
        session_cookie = os.getenv("AOC_SESSION")
    if not _check_cookie(session_cookie):
        raise ValueError("set your session cookie in the .env file")

    import requests

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = requests.get(url, cookies={"session": session_cookie})
    if r.status_code < 200 or r.status_code >= 300:
        raise RuntimeError(f"({r.status_code}) An HTTP error occurred:\n{r.text}")
    return r.text
