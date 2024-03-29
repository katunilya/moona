from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, TypeVar

from fundom import cmap, foldl, future, hof1, pipe, returns_future

from moona.lifespan import LifespanContext

LifespanFunc = Callable[[LifespanContext], future[LifespanContext | None]]
_LifespanHandler = Callable[
    [LifespanFunc, LifespanContext], future[LifespanContext | None]
]


def compose(h1: _LifespanHandler, h2: _LifespanHandler) -> LifespanHandler:
    """Compose 2 `LifespanHandler`s into one.

    Args:
        h1 (_LifespanHandler): to run first.
        h2 (_LifespanHandler): to run second.

    Returns:
        LifespanHandler: resulting handler.
    """

    def handler(
        final: LifespanFunc, ctx: LifespanContext
    ) -> future[LifespanContext | None]:
        _h1 = hof1(h1)
        _h2 = hof1(h2)
        func = _h1(_h2(final))
        return func(ctx)

    return LifespanHandler(handler)


@dataclass(frozen=True, slots=True)
class LifespanHandler:
    """Abstraction over function that hander `LifespanContext`."""

    _handler: Callable[[LifespanContext], future[LifespanContext | None]]

    def __call__(  # noqa
        self, nxt: LifespanFunc, ctx: LifespanContext
    ) -> future[LifespanContext | None]:
        return returns_future(self._handler)(nxt, ctx)

    def __init__(self, handler: _LifespanHandler) -> None:
        object.__setattr__(self, "_handler", handler)

    def compose(self, h: _LifespanHandler) -> LifespanHandler:
        """Compose 2 `LifespanHandler`s into one.

        Args:
            h2 (_LifespanHandler): to run next.

        Returns:
            LifespanHandler: resulting handler.
        """
        return compose(self, h)

    def __rshift__(self, h: _LifespanHandler) -> LifespanHandler:
        return compose(self, h)


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def handler(func: _LifespanHandler) -> LifespanHandler:
    """Decorator that converts function to LifespanHandler callable."""
    return LifespanHandler(func)


def handle_func(func: LifespanFunc) -> LifespanHandler:
    """Converts `LifespanFunc` to `LifespanHandler`.

    Args:
        func (LifespanFunc): to convert to `LifespanHandler`.

    Returns:
        LifespanHandler: result.
    """

    @handler
    async def _handler(
        nxt: LifespanFunc, ctx: LifespanContext
    ) -> LifespanContext | None:
        match await func(ctx):
            case None:
                return None
            case LifespanContext() as _ctx:
                return await nxt(_ctx)

    return _handler


def handle_func_sync(
    func: Callable[[LifespanContext], LifespanContext | None]
) -> LifespanHandler:
    """Converts sync `LifespanFunc` to `LifespanHandler`.

    Args:
        func (Callable[[LifespanContext], LifespanContext | None]): to convert to
        `LifespanHandler`.

    Returns:
        LifespanHandler: result.
    """

    @handler
    async def _handler(
        nxt: LifespanFunc, ctx: LifespanContext
    ) -> LifespanContext | None:
        match func(ctx):
            case None:
                return None
            case LifespanContext() as _ctx:
                return await nxt(_ctx)

    return _handler


def __choose_reducer(f: LifespanFunc, s: LifespanFunc) -> LifespanFunc:
    @future.returns
    async def func(ctx: LifespanContext) -> LifespanFunc:
        _ctx = deepcopy(ctx)
        match await f(_ctx):
            case None:
                return await s(ctx)
            case some:
                return some

    return func


def choose(handlers: list[LifespanHandler]) -> LifespanHandler:
    """Iterate though handlers till one would return some `LifespanContext`.

    Args:
        handlers (list[LifespanHandler]): to iterate through.

    Returns:
        LifespanHandler: result.
    """

    @handler
    async def _handler(
        nxt: LifespanFunc, ctx: LifespanContext
    ) -> LifespanContext | None:
        match handlers:
            case []:
                return await nxt(ctx)
            case _:
                func: LifespanFunc = (
                    pipe(handlers)
                    .then(cmap(hof1))
                    .then(cmap(lambda h: h(nxt)))
                    .then(foldl(__choose_reducer))
                    .finish()
                )
                return await func(ctx)

    return _handler


def handler1(
    func: Callable[[A, LifespanFunc, LifespanContext], future[LifespanContext | None]]
) -> Callable[[A], LifespanHandler]:
    """Decorator for LifespanHandlers with 1 additional argument.

    Makes it "curried".
    """

    def wrapper(a: A) -> LifespanHandler:
        return LifespanHandler(lambda nxt, ctx: func(a, nxt, ctx))

    return wrapper


def handler2(
    func: Callable[
        [A, B, LifespanFunc, LifespanContext], future[LifespanContext | None]
    ]
) -> Callable[[A, B], LifespanHandler]:
    """Decorator for LifespanHandlers with 2 additional arguments.

    Makes it "curried".
    """

    def wrapper(a: A, b: B) -> LifespanHandler:
        return LifespanHandler(lambda nxt, ctx: func(a, b, nxt, ctx))

    return wrapper


def handler3(
    func: Callable[
        [A, B, C, LifespanFunc, LifespanContext], future[LifespanContext | None]
    ]
) -> Callable[[A, B, C], LifespanHandler]:
    """Decorator for LifespanHandlers with 1 additional argument.

    Makes it "curried".
    """

    def wrapper(a: A, b: B, c: C) -> LifespanHandler:
        return LifespanHandler(lambda nxt, ctx: func(a, b, c, nxt, ctx))

    return wrapper


def skip(_: LifespanContext) -> future[None]:
    """`LifespanFunc` that skips pipeline by returning `None` instead of context.

    Args:
        _ (LifespanContext): ctx we don't care of.

    Returns:
        future[None]: result.
    """
    return future(returns_future(None))


def end(ctx: LifespanContext) -> future[LifespanContext]:
    """`LifespanFunc` that finishes the pipeline of request handling.

    Args:
        ctx (LifespanContext): to end.

    Returns:
        future[LifespanContext]: ended ctx.
    """
    return future(returns_future(ctx))
