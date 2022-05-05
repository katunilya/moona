from typing import Callable, Iterable, Type

import toolz
from pydantic import BaseModel


def decode_header(header: tuple[bytes, bytes]) -> tuple[str, str]:  # noqa
    name, value = header
    return name.decode("UTF-8").lower(), value.decode("UTF-8")


def decode_headers(headers: Iterable[Iterable[bytes]]) -> dict[tuple[str, str]]:  # noqa
    match dict(headers):
        case {}:
            return {}
        case not_empty_headers:
            return toolz.itemmap(decode_header, not_empty_headers)


def decode_utf_8(data: bytes) -> str:  # noqa
    return data.decode("UTF-8")


def encode_utf_8(data: str) -> bytes:  # noqa
    return data.encode("UTF-8")


def serialize(data: BaseModel) -> bytes:  # noqa
    return toolz.pipe(
        data,
        BaseModel.json,
        encode_utf_8,
    )


def deserialize(model: Type[BaseModel]) -> Callable[[bytes], BaseModel]:  # noqa
    return model.parse_raw
