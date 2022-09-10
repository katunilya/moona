from typing import Iterable

from fundom import hof1


@hof1
def decode(encoding: str, data: bytes) -> str:  # noqa
    return data.decode(encoding)


@hof1
def encode(encoding: str, data: str) -> bytes:  # noqa
    return data.encode(encoding)


@hof1
def str_split(separator: str, data: str) -> Iterable[str]:  # noqa
    return data.split(separator)
