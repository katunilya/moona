from dataclasses import dataclass


@dataclass
class Error(Exception):
    """Base class for exception."""

    message: str


@dataclass
class HttpError(Error):
    """Base class for exception sent over http."""

    code: int = 400
