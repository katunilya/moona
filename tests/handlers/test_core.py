import pytest

from mona.core import HTTPContext
from mona.handlers.core import (
    HTTPContextResult,
    choose,
    compose,
    error_handler,
    http_handler,
)
from mona.monads.future import Future
from mona.monads.result import Failure, Result, Success


def test_http_handler(ctx: HTTPContext):
    assert http_handler(Result.successfull)(
        Result.successfull(ctx)
    ) == Result.successfull(ctx)
    assert http_handler(Result.successfull)(Result.failed(ctx)) == Result.failed(ctx)


def test_error_handler(ctx: HTTPContext):
    handler = error_handler(Result.successfull)
    assert handler(Result.successfull(ctx)) == Result.successfull(ctx)
    assert handler(Result.failed(ctx)) == Result.successfull(ctx)


def sync_success_handler(ctx: HTTPContextResult) -> HTTPContextResult:
    return ctx


async def async_success_handler(ctx: HTTPContextResult) -> HTTPContextResult:
    return ctx


def fail_handler(ctx: HTTPContextResult) -> HTTPContextResult:
    return Failure(Exception(ctx.value))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial, funcs, result_type",
    [
        (Success, [], Success),
        (Failure, [], Failure),
        (Success, [fail_handler], Failure),
        (Success, [sync_success_handler], Success),
        (Success, [async_success_handler], Success),
        (Success, [fail_handler, sync_success_handler], Failure),
        (Success, [sync_success_handler, fail_handler], Failure),
        (Success, [sync_success_handler, async_success_handler], Success),
        (Success, [sync_success_handler, sync_success_handler], Success),
        (Success, [async_success_handler, async_success_handler], Success),
        (Success, [async_success_handler, sync_success_handler], Success),
    ],
)
async def test_compose(ctx: HTTPContext, initial, funcs, result_type):
    assert isinstance(
        await (Future.create(ctx) >> initial >> compose(*funcs)), result_type
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial, funcs, result_type",
    [
        (Success, [], Success),
        (Failure, [], Failure),
        (Success, [fail_handler], Success),
        (Success, [sync_success_handler], Success),
        (Success, [async_success_handler], Success),
        (Success, [fail_handler, sync_success_handler], Success),
        (Success, [sync_success_handler, fail_handler], Success),
        (Success, [sync_success_handler, async_success_handler], Success),
        (Success, [sync_success_handler, sync_success_handler], Success),
        (Success, [async_success_handler, async_success_handler], Success),
        (Success, [async_success_handler, sync_success_handler], Success),
    ],
)
async def test_choose(ctx: HTTPContext, initial, funcs, result_type):
    assert isinstance(
        await (Future.create(ctx) >> initial >> choose(*funcs)),
        result_type,
    )
