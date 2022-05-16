from math import factorial, sqrt

from moona import asgi, http


def fibonacci(n: int) -> int:  # noqa
    return int((((1 + sqrt(5)) ** n) - ((1 - sqrt(5))) ** n) / (2**n * sqrt(5)))


def handle_fibonacci(n: int) -> http.HTTPHandler:  # noqa
    return http.text(str(fibonacci(n)))


def handle_factorial(n: int) -> http.HTTPHandler:  # noqa
    return http.text(str(factorial(n)))


http_handler = http.GET >> http.choose(
    [
        http.route("/factorial") >> http.bind_int(handle_factorial),
        http.route("/fibonacci") >> http.bind_int(handle_fibonacci),
    ]
)

app = asgi.create(http_handler=http_handler)
