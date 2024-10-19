from typing import AsyncGenerator

from aiohttp import web

from app.urls import urls
from core.database import close_orm, init_orm
from core.middlewares import exception_middleware, jwt_middleware


async def lifespan(app: web.Application) -> AsyncGenerator:
    print("started")
    await init_orm()
    yield
    await close_orm()
    print("stopped")


app = web.Application(middlewares=[jwt_middleware, exception_middleware])
app.cleanup_ctx.append(lifespan)
app.add_routes(urls)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
