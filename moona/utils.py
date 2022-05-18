from typing import Iterable

from pymon import hof_2


@hof_2
def decode(encoding: str, data: bytes) -> str:  # noqa
    return data.decode(encoding)


@hof_2
def encode(encoding: str, data: str) -> bytes:  # noqa
    return data.encode(encoding)


@hof_2
def str_split(separator: str, data: str) -> Iterable[str]:  # noqa
    return data.split(separator)
