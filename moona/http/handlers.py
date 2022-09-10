from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeVar

from fundom import cmap, foldl, future, hof1, pipe, this_future

from moona.http.context import HTTPContext

HTTPFunc = Callable[[HTTPContext], future[HTTPContext | None]]
_HTTPHandler = Callable[[HTTPFunc, HTTPContext], future[HTTPContext | None]]


def compose(h1: _HTTPHandler, h2: _HTTPHandler) -> HTTPHandler:
    """Compose 2 `HTTPHandler`s into one.

    Args:
        h1 (_HTTPHandler): to run first.
        h2 (_HTTPHandler): to run second.

    Returns:
        HTTPHandler: resulting handler.
    """

    def handler(final: HTTPFunc, ctx: HTTPContext) -> future[HTTPContext | None]:
        _h1 = hof1(h1)
        _h2 = hof1(h2)
        func = _h1(_h2(final))

        match ctx.closed:
            case True:
                return final(ctx)
            case False:
                return func(ctx)

    return HTTPHandler(handler)


@dataclass(frozen=True, slots=True)
class HTTPHandler:
    """Abstraction over function that hander `HTTPContext`."""

    _handler: Callable[[HTTPContext], future[HTTPContext | None]]

    def __call__(  # noqa
        self, nxt: HTTPFunc, ctx: HTTPContext
    ) -> future[HTTPContext | None]:
        return future.returns(self._handler)(nxt, ctx)

    def __init__(self, handler: _HTTPHandler) -> None:
        object.__setattr__(self, "_handler", handler)

    def compose(self, h: _HTTPHandler) -> HTTPHandler:
        """Compose 2 `HTTPHandler`s into one.

        Args:
            h2 (_HTTPHandler): to run next.

        Returns:
            HTTPHandler: resulting handler.
        """
        return compose(self, h)

    def __rshift__(self, h: _HTTPHandler) -> HTTPHandler:
        return compose(self, h)


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def handler(func: _HTTPHandler) -> HTTPHandler:
    """Decorator that converts function to HTTPHandler callable."""
    return HTTPHandler(func)


def handle_func(func: HTTPFunc) -> HTTPHandler:
    """Converts `HTTPFunc` to `HTTPHandler`.

    Args:
        func (HTTPFunc): to convert to `HTTPHandler`.

    Returns:
        HTTPHandler: result.
    """

    @handler
    async def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
        match await func(ctx):
            case None:
                return None
            case HTTPContext() as _ctx:
                match _ctx.closed:
                    case True:
                        return _ctx
                    case False:
                        return await nxt(_ctx)

    return _handler


def handle_func_sync(func: Callable[[HTTPContext], HTTPContext | None]) -> HTTPHandler:
    """Converts sync `HTTPFunc` to `HTTPHandler`.

    Args:
        func (Callable[[HTTPContext], HTTPContext | None]): to convert to `HTTPHandler`.

    Returns:
        HTTPHandler: result.
    """

    @handler
    async def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
        match func(ctx):
            case None:
                return None
            case HTTPContext() as _ctx:
                match _ctx.closed:
                    case True:
                        return _ctx
                    case False:
                        return await nxt(_ctx)

    return _handler


def __choose_reducer(f: HTTPFunc, s: HTTPFunc) -> HTTPFunc:
    @future.returns
    async def func(ctx: HTTPContext) -> HTTPFunc:
        match await f(ctx):
            case None:
                return await s(ctx)
            case some:
                return some

    return func


def choose(handlers: list[HTTPHandler]) -> HTTPHandler:
    """Iterate though handlers till one would return some `HTTPContext`.

    Args:
        handlers (list[HTTPHandler]): to iterate through.

    Returns:
        HTTPHandler: result.
    """

    @handler
    async def _handler(nxt: HTTPFunc, ctx: HTTPContext) -> HTTPContext | None:
        match handlers:
            case []:
                return await nxt(ctx)
            case _:
                func: HTTPFunc = (
                    pipe(handlers)
                    .then(cmap(hof1))
                    .then(cmap(lambda h: h(nxt)))
                    .then(foldl(__choose_reducer, skip))
                    .finish()
                )
                return await func(ctx)

    return _handler


def handler1(
    func: Callable[[A, HTTPFunc, HTTPContext], future[HTTPContext | None]]
) -> Callable[[A], HTTPHandler]:
    """Decorator for HTTPHandlers with 1 additional argument.

    Makes it "curried".
    """

    def wrapper(a: A) -> HTTPHandler:
        return HTTPHandler(lambda nxt, ctx: func(a, nxt, ctx))

    return wrapper


def handler2(
    func: Callable[[A, B, HTTPFunc, HTTPContext], future[HTTPContext | None]]
) -> Callable[[A, B], HTTPHandler]:
    """Decorator for HTTPHandlers with 2 additional arguments.

    Makes it "curried".
    """

    def wrapper(a: A, b: B) -> HTTPHandler:
        return HTTPHandler(lambda nxt, ctx: func(a, b, nxt, ctx))

    return wrapper


def handler3(
    func: Callable[[A, B, C, HTTPFunc, HTTPContext], future[HTTPContext | None]]
) -> Callable[[A, B, C], HTTPHandler]:
    """Decorator for HTTPHandlers with 1 additional argument.

    Makes it "curried".
    """

    def wrapper(a: A, b: B, c: C) -> HTTPHandler:
        return HTTPHandler(lambda nxt, ctx: func(a, b, c, nxt, ctx))

    return wrapper


def skip(_: HTTPContext) -> future[None]:
    """`HTTPFunc` that skips pipeline by returning `None` instead of context.

    Args:
        _ (HTTPContext): ctx we don't care of.

    Returns:
        future[None]: result.
    """
    return this_future(None)


def end(ctx: HTTPContext) -> future[HTTPContext]:
    """`HTTPFunc` that finishes the pipeline of request handling.

    Args:
        ctx (HTTPContext): to end.

    Returns:
        future[HTTPContext]: ended ctx.
    """
    return this_future(ctx)
