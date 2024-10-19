from typing import Awaitable, Callable

from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from core.settings import Settings


@web.middleware
async def exception_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    try:
        return await handler(request)
    except web.HTTPException as ex:
        reason = ex.reason if ex.reason else "Unknown Error"
        status = ex.status if ex.status else 500
        return web.json_response({"error": reason}, status=status)


jwt_middleware = JWTMiddleware(
    Settings.SECRET_KEY,
    credentials_required=False,
    algorithms=Settings.ALGORITHM,
)
