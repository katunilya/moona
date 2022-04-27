from typing import Iterable

import toolz


def decode_header(header: tuple[bytes, bytes]) -> tuple[str, str]:  # noqa
    name, value = header
    return name.decode("UTF-8").lower(), value.decode("UTF-8")


def decode_headers(headers: Iterable[Iterable[bytes]]) -> dict[tuple[str, str]]:  # noqa
    match dict(headers):
        case {}:
            return {}
        case not_empty_headers:
            return toolz.itemmap(decode_header, not_empty_headers)
