import jwt
from aiohttp import web

from app.models import Advertisement, User
from app.schemas import (CreateAdvertisementSchema, CreateUserTokenSchema,
                         PartialUpdateAdvertisementSchema)
from app.security import get_password_hash, jwt_required
from app.service import Service
from app.validation import validate_request
from core.database import DbSession
from core.settings import Settings

service = Service(DbSession())


class CreateUserView(web.View):
    async def post(self) -> web.Response:
        validated_data = await validate_request(self.request, CreateUserTokenSchema)
        validated_data["password"] = get_password_hash(validated_data["password"])
        response = await service.add(User, validated_data)
        return web.json_response(response, status=201)


class CreateTokenView(web.View):
    async def post(self) -> web.Response:
        validated_data = await validate_request(self.request, CreateUserTokenSchema)
        user_id = await service.verify_user_and_get_id(validated_data)
        token = jwt.encode({"user_id": user_id}, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return web.json_response({"token": token}, status=201)


class AdvertisementViewSet(web.View):
    async def get(self) -> web.Response:
        adv_id = self.request.match_info.get("id")
        if adv_id:
            response = await service.get_adv_by_id(int(adv_id))
            return web.json_response(response, status=200)
        response = await service.get_all_advs()
        return web.json_response(response, status=200)

    @jwt_required
    async def post(self) -> web.Response:
        validated_data = await validate_request(self.request, CreateAdvertisementSchema)
        validated_data["creator"] = self.request["payload"]["user_id"]
        response = await service.add(Advertisement, validated_data)
        return web.json_response(response, status=201)

    @jwt_required
    async def patch(self) -> web.Response:
        adv_id = int(self.request.match_info.get("id"))
        await service.verify_adv_creator(self.request, adv_id)
        validated_data = await validate_request(self.request, PartialUpdateAdvertisementSchema)
        response = await service.update_adv(adv_id, validated_data)
        return web.json_response(response, status=200)

    @jwt_required
    async def put(self) -> web.Response:
        adv_id = int(self.request.match_info.get("id"))
        await service.verify_adv_creator(self.request, adv_id)
        validated_data = await validate_request(self.request, CreateAdvertisementSchema)
        response = await service.update_adv(adv_id, validated_data)
        return web.json_response(response, status=200)

    @jwt_required
    async def delete(self) -> web.Response:
        adv_id = int(self.request.match_info.get("id"))
        await service.verify_adv_creator(self.request, adv_id)
        response = await service.delete_adv(adv_id)
        return web.json_response(response, status=204)
