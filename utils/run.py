from typing import Any, Callable, List

from .input import read_input, Converter, T

__all__ = ("run",)

Func = Callable[[List[T]], Any]


def run(splitter: str = "\n", *, c: Converter = str, override: str = None) -> Func:
    def wrapper(func: Func) -> Func:
        g = func.__globals__
        if g["__name__"] == "__main__": # prevent this from running functions when imported
            data = read_input(g["__file__"], splitter, c=c, override=override)
            result = func(data)
            print(f"{func.__name__}:", result)
        return func
    return wrapper
