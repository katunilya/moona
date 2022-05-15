import httpx
from pymon import Pipe

from moona import asgi, lifespan


def cheer(ctx: lifespan.LifespanContext) -> lifespan.LifespanContext:
    print("Cheers to our server!!!")
    return ctx


async def ping_anime(ctx: lifespan.LifespanContext) -> lifespan.LifespanContext:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://animechan.vercel.app/api/random")
    data = response.json()
    print(f"Quote from {data['anime']} by {data['character']}: {data['quote']}")
    return ctx


async def bye(ctx: lifespan.LifespanContext) -> lifespan.LifespanContext:
    print("See you soon server!!!")
    return ctx


app = asgi.create(
    startup_handler=lifespan.handle_func(lambda ctx: Pipe(cheer(ctx)) >> ping_anime),
    shutdown_handler=lifespan.handle_func(bye),
)

# INFO:     Started server process [2394]
# INFO:     Waiting for application startup.
# Cheers to our server!!!
# Quote from Shingeki no Kyojin by Levi Ackerman: A lot of the times, you're going into
# a situation you know nothing about. So what you need is to be quick to act... and make
# tough decisions in worst-case scenarios.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Shutting down
# INFO:     Waiting for application shutdown.
# See you soon server!!!
# INFO:     Application shutdown complete.
# INFO:     Finished server process [2394]
