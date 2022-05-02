import asyncio

from mona.monads import Future


async def async_inc(x: int) -> int:
    return x + 1


def sync_square(x: int) -> int:
    return x**2


async def main():
    # Future can be directly created from awaitable
    f = Future(async_inc(2))

    print(await f)  # 3

    # Future can be also created from present value via Future.create
    f = Future.create(3)  # create some Future from sync value

    composition = Future.compose(
        async_inc,
        async_inc,
        sync_square,
    )  # (x + 1 + 1)^2
    # composition: (int) -> Future[int] (which is nearly the same as Awaitable[int])

    # Future monad overrides `>>` operator for applying sync or async functions
    result = await (f >> composition)

    print(result)  # 25


if __name__ == "__main__":
    asyncio.run(main())

# can be run as-is
