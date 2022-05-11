from math import factorial, sqrt

import mona
from mona.core import HTTPContext
from mona.handlers import (
    GET,
    bind_body_text_async,
    choose,
    compose,
    get_body_text_async,
    http,
    route,
    send_body_async,
)
from mona.handlers.core import HTTPContextResult
from mona.monads.func import FutureFunc
from mona.monads.future import Future
from mona.monads.pipe import Pipeline
from mona.monads.result import Result


def fibonacci(n: int) -> int:  # noqa
    return int((((1 + sqrt(5)) ** n) - ((1 - sqrt(5))) ** n) / (2**n * sqrt(5)))


h = FutureFunc(get_body_text_async).then(int).then(fibonacci).then(str)


def fibonacci_handler(ctx: HTTPContext) -> Future[HTTPContextResult]:  # noqa
    return (
        Pipeline(ctx)
        .then(GET)
        .then(route("/fibonacci"))
        .then_future(bind_body_text_async())
        .then_future(send_body_async)
    )


factorial_handler = compose(
    GET,
    route("/factorial"),
    bind_body_text_async(
        compose(
            get_body_text_async,
            Result.if_ok_safe(int),
            Result.if_ok_safe(factorial),
            Result.if_ok_safe(str),
        )
    ),
    send_body_async,
)

app = mona.create(
    compose(
        http,
        choose(
            fibonacci_handler,
            factorial_handler,
        ),
    )
)
