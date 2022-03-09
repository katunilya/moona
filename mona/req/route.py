import re
from typing import Match, Optional, Pattern

from mona import context, state


def on_route(pattern: str) -> context.Handler:
    """If request `path` is the same as `pattern` than context is valid."""
    pattern = pattern.strip("/")

    def _handler(ctx: context.Context) -> context.StateContext:
        return state.valid(ctx) if pattern == ctx.path else state.invalid(ctx)

    return _handler


def on_subroute(pattern: str) -> context.Handler:
    """Returns valid context without subroute part of it if `pattern` equals `path`."""
    pattern = pattern.strip("/")

    def _handler(ctx: context.Context) -> context.Context:
        if ctx.path.startswith(pattern):
            subroute = len(pattern)
            ctx.path = ctx.path[subroute:].strip("/")
            return state.valid(ctx)

        return state.invalid(ctx)

    return _handler


def on_ciroute(pattern: str) -> context.Handler:
    """Case insensitive version of `on_route`."""
    pattern = pattern.strip("/").lower()

    def _handler(ctx: context.Context) -> context.Context:
        return state.valid(ctx) if ctx.path.lower() == pattern else state.invalid(ctx)

    return _handler


def on_cisubroute(pattern: str) -> context.Handler:
    """Case insensitive version of `on_subroute`."""
    pattern = pattern.strip("/").lower()

    def _handler(ctx: context.Context) -> context.Context:
        if ctx.path.lower().startswith(pattern):
            subroute_len = len(pattern)
            ctx.path = ctx.path[subroute_len:].strip("/")
            return state.valid(ctx)
        return state.invalid(ctx)

    return _handler
