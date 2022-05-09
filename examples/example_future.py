import asyncio

from mona.monads import Future


async def async_inc(x: int) -> int:  # noqa
    return x + 1


def sync_square(x: int) -> int:  # noqa
    return x**2


async def main():  # noqa

    result = await (
        Future(async_inc(3))
        .then(sync_square)
        .then_future(async_inc)
        .then_future(async_inc)
        .then(sync_square)
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())

# can be run as-is
