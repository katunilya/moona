import urllib.parse as urlparser

from toolz.functoolz import pipe

from mona import context


def parse_query(ctx: context.Context) -> context.Context:
    """Parses query from url and places it as dictionary to context."""
    ctx.query = pipe(
        ctx.query_string,
        lambda byte_string: byte_string.decode("utf-8"),
        urlparser.parse_qs,
    )
    return ctx
