from typing import Callable

import bcrypt
from aiohttp import web


def get_password_hash(user_password: str) -> str:
    user_password = user_password.encode()
    hashed_password = bcrypt.hashpw(user_password, bcrypt.gensalt())
    hashed_password = hashed_password.decode()
    return hashed_password


def verify_password(user_password: str, hashed_password: str) -> bool:
    user_password = user_password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(user_password, hashed_password)


def jwt_required(view: Callable) -> Callable:
    async def wrapper(self, *args, **kwargs) -> web.Response:
        if self.request.get('payload') is None:
            raise web.HTTPUnauthorized(reason="authentication credentials not provided", content_type="application/json")
        return await view(self, *args, **kwargs)

    return wrapper
