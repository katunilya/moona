from typing import Iterable

import orjson
import toolz
from pydantic import BaseModel

from mona.monads.result import Result


def decode_header(header: tuple[bytes, bytes]) -> tuple[str, str]:  # noqa
    name, value = header
    return name.decode("UTF-8").lower(), value.decode("UTF-8")


def decode_headers(headers: Iterable[Iterable[bytes]]) -> dict[tuple[str, str]]:  # noqa
    match dict(headers):
        case {}:
            return {}
        case not_empty_headers:
            return toolz.itemmap(decode_header, not_empty_headers)


@Result.safe
def encode_utf_8(s: str) -> bytes:  # noqa
    return s.encode("UTF-8")


@Result.safe
def serialize(obj: object) -> bytes:  # noqa
    match obj:
        case BaseModel() as base_model:
            return orjson.dumps(base_model.dict())
        case other:
            return orjson.dumps(other)
