import json

from mona import context


def parse_body_json(ctx: context.Context) -> context.Context:
    """When raw request body is not `None` try parse it to `Dict`."""
    if ctx.raw_request_body is not None:
        ctx.request_body = json.loads(ctx.raw_request_body)

    return ctx
