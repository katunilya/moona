import mona
from mona.core import LifespanContext
from mona.handlers.lifespan import lifespan_async


def on_startup(ctx: LifespanContext) -> LifespanContext:  # noqa
    print("Server startup!")
    return ctx


def on_shutdown(ctx: LifespanContext) -> LifespanContext:  # noqa
    print("Server shutdown!")
    return ctx


app = mona.create(lifespan_async(on_startup, on_shutdown))

# INFO:     Started server process [7737]
# INFO:     Waiting for application startup.
# Server startup!
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# ^C
# INFO:     Shutting down
# INFO:     Waiting for application shutdown.
# Server shutdown!
# INFO:     Application shutdown complete.
# INFO:     Finished server process [7737]
