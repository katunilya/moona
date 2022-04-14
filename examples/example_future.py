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
