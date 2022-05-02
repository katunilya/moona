# mona

`mona` is an ASGI server framework that provides a set of guidelines on software
development inspired by functional programming and monads. It's core design is
hugely inspired by Finite State Machines and Railroad Architecture approach.

## ✨ Overview

`mona` provides abstractions for so called `State` monad and `Future` monad.
`State` monad provides functionality of FSM with a few pre-defined states:

- `Right` for processing going right way;
- `Wrong` for processing going wrong way;
- `Error` for processing stopped due to error;
- `Final` for processing that should not be continued;

Example:

```python
import dataclasses

from mona import state


@dataclasses.dataclass
class User:
    name: str
    age: int
    role: str


__users = [
    User("John", 21, "admin"),
    User("Maria", 40, "modetator"),
    User("Ivan", 28, "user"),
    User("Alex", 13, "user"),
    User("Nicole", 19, "user"),
]


def get_admin(name: str) -> state.ESafe[User]:
    match next((u for u in __users if u.name == name), None):
        case User(role="admin") as user:
            return state.Right(user)
        case _:
            return state.Error(Exception(f"User {name} is not admin!"))


print(get_admin("John"))
print(get_admin("Ivan"))

# can be run as-is
```

`Future` core feature is composition of sync and async function into one async:

```python
import asyncio

from mona import future


async def async_inc(x: int) -> int:
    return x + 1


def sync_square(x: int) -> int:
    return x**2


async def main():
    f = future.from_value(3)  # create some Future from sync value

    composition = future.compose(async_inc, async_inc, sync_square)  # (x + 1 + 1)^2

    result = await future.bind(composition, f)

    print(result)  # 25

    # there is another syntax for exactly the same thing
    result = await (future.from_value(3) >> async_inc >> async_inc >> sync_square)

    print(result)  # 25


if __name__ == "__main__":
    asyncio.run(main())

# can be run as-is
```

This are core concepts of `mona`. Based on them entire application is just a so
called `Handler` - sync or async function that takes `Context` of some state and
return `Context` of some state. The simples server written in `mona`:

```python
from mona import asgi, future, req, res

app = asgi.create(
    future.compose(
        req.on_http,
        res.set_body_text("Hello!"),
        res.send_start,
        res.send_body,
    )
)

# run with unicorn
# 
# $ curl http://localhost:8000/
# Hello!%
```

This example provides server that return `Hello!` for any request. See more
examples in [examples folder](/examples/). Also check out full API specification
on official [Documentation Page](https://katunilya.github.io/mona/).

> Documentation is generated via [handsdown](https://github.com/vemel/handsdown)

## ⬇️ Install

`mona` is currently at a very dynamic and stormy development stage and lacks
multiple important features, so it is not published in PyPi currently and can be
installed as raw package from GitHub directly.

I suggest using [poetry](https://github.com/python-poetry/poetry) for package
management. Having project environment setup execute:

```sh
poetry add git+https://github.com/katunilya/mona
```

Another way is to build package from source:

```sh
git clone https://github.com/katunilya/mona
cd mona
poetry build
pip install dist/mona-0.2.2.tar.gz
```

## 🏗️ Develop

Fork repository. `poetry` is required for project development as it provides
simple way of managing dependencies and environment. To setup a project run:

```sh
make setup
```

This will create and activate environment, install all required dependencies and
setup `pre-commit`.

Now you are ready to bring your ideas to the project. Check out [Contribution
Guidelines](/CONTRIBUTING.md) for more information on project development.
