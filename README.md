<h1 align="center">🌙 moona</h2>

`moona` is an ASGI server framework that provides a set of guidelines on software
development inspired by functional programming and monads. It's core design is
hugely inspired by Finite State Machines and Railroad Architecture approach.

## 🤔 Motivation

Before we dive into examples and feature explanation I want to explain
motivation behind the project. There are multiple statements I had in mind so
let's check some of my thoughts.

### There is always right way to write a function

One very important thing about function we have is it's interface which we often
think not much of. I believe there are a few ideas you should follow writing
functions:

- Most important argument of the function is data that will be changed
- Most important argument must be the last one
- Best function is one that takes only one argument
- Function the requires multiple arguments should be applied partially or be HOF

> When I say "changed" I clearly understand that it's much easier to work with
> immutable data, however in Python nearly everything is mutable, but this
> "feature" is a good marker of most important argument.

This "requirements" I follow in `moona` are important for better usage of such
functional tools like _function composition_ and _curring_.

In this way all the functions must be just:

- Single-argument functions
- Higher-order functions that return single-argument functions

If we operate with single-argument functions we can apply them sequentially
(compose). In case we need to provide more than one argument we should use HOF.

🔎 Example:

```py
# ❌ this function is bad as we can't properly parametrize it for composition or
# pipeline usage.
encode = str.encode

# ✅ this function is good as it is HOF that accepts single `str` argument which
# is changed after we pass encoding key.
better_encode = lambda encoding: lambda s: return s.encode(encoding)

# also we can easier produce single-argument composition-ready functions
encode_utf_8 = better_encode("UTF-8")
```

> ⚠️ Do not use lambdas for such cases as it is harder to debug them and you
> provide no type hinting.

### Computer should do only what programmer asked

Developers love using frameworks that get rid of underlying details of
implementation and provide friendly interface for solving common problems. The
only issue with this approach is that we rarely directly know what exactly is
going on and when we face some bug or problem it's hard to find out whether it
is actual bug or feature that we had no idea of.

IMHO ASGI specification is not something hard to grasp and understand and it is
important to understand application lifecycle and events that happen during
service execution.

In this way `moona` does nothing except what you said. If you forgot to set a
header than this is your problem, if you forgot to send a body, this is your
problem (well, `moona` does it for you actually, but that is required for
persisting successful processing path).

### Everything is monad

> Monad is a monoid in the monoidal category of endofunctors equipped with
> functor composition as its product.

This is a joke (or not), but there are multiple good reasons why to use monads
instead of some other common approaches of handling different cases in code.

**`Exception` handling** is a huge problem in many programming languages. Common
approach is try-catch (or except) expressions, that wrap code that might raise
error. But for it to work developer must inform you of `Exception`s that might
be raised and you should find and remember to handle them all or explain why you
don't handle something (at least to future-self). Code becomes much more verbose
and complex. In Python you even loose in performance (but if you care about
performance you should consider another tool). Also try-except-finally by itself
is shallow if-elif-else expression which also makes your code too complex.

Before we wen't too far let's sum up 2 problems of try-except approach:

- No explicit explanation of possible raise `Exception`s (only via docstrings)
- Code becomes to complex if we handle `Exception`s via try-except blocks

> Some of you might say that in Java for example we explicitly provide
> information about raised `Exception`s. Yes, but if it is good than why we have
> `@SneakyThrows` annotation? Because we are lazy and don't really like this
> try-catch blocks.

Another good example of infinite checks - `None` value. Often we do something
only if some other function previously returned some actual result.

`moona` uses monads from [`pymon`](https://github.com/katunilya/pymon) (under development).

### Be declarative means you named your child good

I'm in love with declarative code, because with that I feel myself as an author
that tells a good-written story instead of instruction for building spaceship on
toilet paper.

However most enterprise languages are imperative and decorativeness becomes just
another code style that hides all imperative instructions under well named
functions and elegant constructions.

This is the Saint Graal of `moona` underlying concepts. Code should be written as
some pipeline that tells what actually happens in the system and what we get as
a result. Monads, single-argument functions, curring are just tools that can
provide this experience in good hands.

No we are ready to get right to `moona`.

## ASGI

ASGI stand for Asynchronous Server Gateway. This is not some framework. It is
just some specification that tells how asynchronous server must be written in
Python. So I suggest reading [ASGI
Specification](https://asgi.readthedocs.io/en/latest/specs/main.html)

Currently `moona` supports to kinds of ASGI scope - "http" and "lifespan".

### HTTP Handlers

HTTPHandler is a function with interface `(nxt: HTTPFunc, ctx: HTTPContext) ->
Future[HTTPContext | None]`

In `moona` `HTTPHandler` is actually callable class. This is required for
providing `>>` syntax for composing multiple `HTTPHandler`s.

Short list of handlers of `moona`:

- Response Header `HTTPHandler`s

  - `header` - sets some header to response;
  - `content_type` - sets "Content-Type" response header;

- Request header `HTTPHandler`s

  - `has_header` - checks if request has some header;

- Response Status Code `HTTPHandler`s

  - `set_status` - sets status code;
  - `set_ok` - sets 200 OK status code;
  - `ok` - sets 200 OK status code and responds with passed value;

- Response Body `HTTPHandler`s

  - `set_raw` - sets response body from bytes;
  - `set_text` - sets response body from string;
  - `set_json` - sets response body from
    [pydantic](https://github.com/samuelcolvin/pydantic/) `BaseModel`;
  - `raw` - respond with raw bytes;
  - `text` - respond with string;
  - `json` - respond with json string form
    [pydantic](https://github.com/samuelcolvin/pydantic/) `BaseModel`;

- Request Body `HTTPHandler`s

  - `bind_raw` - run some `HTTPHandler` that processes bytes;
  - `bind_text` - run some `HTTPHandler` that processes string;
  - `bind_json` - run some `HTTPHandler` that processes
    [pydantic](https://github.com/samuelcolvin/pydantic/) `BaseModel`;
  - `bind_int` - run some `HTTPHandler` that processes integer;
  - `bind_dict` - run some `HTTPHandler` that processes dictionary;

- Request Route `HTTPHandler`s

  - `route` - process request on exact route;
  - `route_ci` - process request on case-insensitive route;
  - `subroute` - process request on exact subroute;
  - `subroute_ci` - process request on case-insensitive subroute;

- Request Method `HTTPHandler`s

  - `method` - check if request has corresponding HTTP Method;
  - `GET` - check if request has "GET" HTTP Method;
  - `POST` - check if request has "POST" HTTP Method;
  - `PUT` - check if request has "PUT" HTTP Method;
  - `PATCH` - check if request has "PATCH" HTTP Method;
  - `DELETE` - check if request has "DELETE" HTTP Method;
  - `HEAD` - check if request has "HEAD" HTTP Method;
  - `OPTIONS` - check if request has "OPTIONS" HTTP Method;
  - `TRACE` - check if request has "TRACE" HTTP Method;
  - `CONNECT` - check if request has "CONNECT" HTTP Method;

- ASGI Events `HTTPHandler`s

  - `receive` - "http.request" Receive Event;
  - `start` - "http.request.start" Send Event;
  - `respond` - "http.request.body" Send Event;

Example if simple application that calculates `n`th Fibonacci number and `n!` on
corresponding "GET" routes:

```python
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

```

See more examples in [examples folder](/examples/). Also check out full API
specification on official [Documentation
Page](https://katunilya.github.io/moona/).

> Documentation is generated via [handsdown](https://github.com/vemel/handsdown)

## ⬇️ Install

`moona` is currently at a very dynamic and stormy development stage and lacks
multiple important features, so it is not published in PyPi currently and can be
installed as raw package from GitHub directly.

I suggest using [poetry](https://github.com/python-poetry/poetry) for package
management. Having project environment setup execute:

```sh
poetry add git+https://github.com/katunilya/moona
```

Another way is to build package from source:

```sh
git clone https://github.com/katunilya/moona
cd moona
poetry build
pip install dist/moona-0.2.2.tar.gz
```

## 🏗️ Develop

Fork repository. `poetry` is required for project development as it provides
simple way of managing dependencies and environment. To setup a project run:

```sh
make setup
```

This will create and activate environment, install all required dependencies and
setup `pre-commit`.

### `Makefile`

Other `Makefile` features:

- `create_env`: create virtual environment;
- `activate_env`: activate virtual environment;
- `update_deps`: update dependencies with `poetry`;
- `deps_install_no_dev`: install all dependencies except required for
  development with `poetry`;
- `deps_install`: install all dependencies with `poetry`;
- `deps_export`: export dependencies into `requirements.txt`;
- `check_flake8`: check repository with `flake8`;
- `check_isort`: check repository with `isort`;
- `test`: run `pytest` tests;
- `check`: run all previous checks;
- `setup_pre_commit`: setup `pre-commit` hooks;
- `docs`: generate new documentation source files;
- `setup`: setup repository for development;

Now you are ready to bring your ideas to the project. Check out [Contribution
Guidelines](/CONTRIBUTING.md) for more information on project development.
