from json import JSONDecodeError
from typing import Dict

from aiohttp import web
from pydantic import BaseModel, ValidationError


async def validate_request(request: web.Request, schema: BaseModel) -> Dict[str, str]:
    try:
        request_data = await request.json()
    except JSONDecodeError:
        raise web.HTTPBadRequest(reason="body can not be empty", content_type="application/json")
    try:
        return schema(**request_data).model_dump()
    except ValidationError as e:
        error = e.errors()[0]
        error.pop("ctx", None)
        raise web.HTTPBadRequest(reason=error, content_type="application/json")
