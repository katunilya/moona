from functools import reduce
from typing import Awaitable, Callable

from mona import context
from mona.context import Context
from mona.monads import future
from mona.monads.maybe import Maybe, Some

ContextFunc = Callable[[Maybe[Context]], Maybe[Context] | Awaitable[Maybe[Context]]]


def handler(
    func: Callable[[Context], Maybe[Context] | Awaitable[Maybe[Context]]]
) -> ContextFunc:
    """Mandatory decorator for ContextFunc.

    This decorator provides `Maybe` monad handling logic for `ContextFunc` out of the
    box. With it you don't need to explicitly mention that handler excepts only `Some`
    `Context`. In other words it transforms function that accepts `Context` to function
    that accepts `Maybe[Context]` and will be processed only when one is
    `Some[Context]`.

    Example::

            @handler
            def h(ctx: Context) -> Maybe[Context]:
               ...

            h(Some(ctx))  # executed
            h(Nothing())  # not executed

    Args:
        func (Callable[[Context], Maybe[Context] | Awaitable[Maybe[Context]]]): to be
        decorated

    Returns:
        ContextFunc: ready-to-use Context Func
    """

    def _func(ctx: Maybe[Context]) -> Maybe[Context]:
        return ctx >> func

    return _func


def __next_on_some(current_func: ContextFunc, next_func: ContextFunc) -> ContextFunc:
    @handler
    async def _func(ctx: Context) -> Maybe[Context]:
        match await (future.from_value(ctx) >> context.copy >> Some >> current_func):
            case Some(value):
                return value
            case _:
                return await (future.from_value(ctx) >> Some >> next_func)

    return _func


def choose(*funcs: ContextFunc) -> ContextFunc:
    """Logical combinator of `ContextFunc`s catching first `Some` result.

    Sequentially executes passed `ContextFunc`s till one of them returns `Some[Context]`
    which would be returned right away.

    In case `func` is empty iterable `future.identity` function is returns so `choose`
    won't critically affect application behavior.

    Example::

            c = choose(
                func_1,  # returns Nothing
                func_2,  # returns Some
                func_3,  # returns Some
            )

            result = await (future.from_value(ctx) >> c)  # result of func_2

    Returns:
        ContextFunc: composed function
    """
    match funcs:
        case ():
            return future.identity
        case _:
            return reduce(__next_on_some, funcs)
