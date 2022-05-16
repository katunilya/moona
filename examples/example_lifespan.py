import httpx

from moona import asgi, lifespan


@lifespan.handle_func_sync
def cheer(ctx: lifespan.LifespanContext) -> lifespan.LifespanContext:  # noqa
    print("Cheers to our server!!!")
    return ctx


@lifespan.handle_func
async def anime_quote(  # noqa
    ctx: lifespan.LifespanContext,
) -> lifespan.LifespanContext:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://animechan.vercel.app/api/random")
    data = response.json()
    print(f"Quote from {data['anime']} by {data['character']}: {data['quote']}")
    return ctx


@lifespan.handle_func_sync
def bye(ctx: lifespan.LifespanContext) -> lifespan.LifespanContext:  # noqa
    print("See you soon server!!!")
    return ctx


app = asgi.create(
    startup_handler=cheer >> anime_quote,
    shutdown_handler=bye,
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
