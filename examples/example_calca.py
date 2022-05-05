from math import factorial, sqrt

import mona
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
from mona.monads import Result


def fibonacci(n: int) -> int:  # noqa
    return int((((1 + sqrt(5)) ** n) - ((1 - sqrt(5))) ** n) / (2**n * sqrt(5)))


fibonacci_handler = compose(
    GET,
    route("/fibonacci"),
    bind_body_text_async(
        compose(
            get_body_text_async,
            Result.safely_bound(int),
            Result.safely_bound(fibonacci),
            Result.safely_bound(str),
        )
    ),
    send_body_async,
)

factorial_handler = compose(
    GET,
    route("/factorial"),
    bind_body_text_async(
        compose(
            get_body_text_async,
            Result.safely_bound(int),
            Result.safely_bound(factorial),
            Result.safely_bound(str),
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
