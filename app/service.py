from aiohttp import web
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Advertisement, User
from app.security import verify_password


class Service:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
        self, model: type[User] | type[Advertisement], validated_data: dict[str, str]
    ) -> dict[str, str | int]:
        instance = model(**validated_data)
        async with self.session as session:
            try:
                session.add(instance)
                await session.commit()
                return instance.to_dict()
            except IntegrityError:
                await session.rollback()
                raise web.HTTPConflict(reason="email already exists", content_type="application/json")

    async def verify_user_and_get_id(self, data: dict[str, str]) -> int:
        email, password = data["email"], data["password"]
        async with self.session as session:
            user = await session.execute(select(User).where(User.email == email))
            user = user.scalar_one_or_none()
        if not user:
            raise web.HTTPUnauthorized(reason="user not found", content_type="application/json")
        if not verify_password(password, user.password):
            raise web.HTTPUnauthorized(reason="wrong password", content_type="application/json")
        return user.id

    async def verify_adv_creator(self, request: web.Request, adv_id: int) -> None:
        adv = await self.get_adv_instance_by_id(adv_id)
        if adv.creator != request["payload"]["user_id"]:
            raise web.HTTPForbidden(reason="Forbidden", content_type="application/json")

    async def get_adv_instance_by_id(self, adv_id: int) -> Advertisement:
        async with self.session as session:
            adv = await session.execute(select(Advertisement).where(Advertisement.id == adv_id))
            adv = adv.scalar_one_or_none()
            if not adv:
                raise web.HTTPNotFound(reason="advertisement not found", content_type="application/json")
            return adv

    async def get_adv_by_id(self, adv_id: int) -> dict[str, str | int]:
        adv = await self.get_adv_instance_by_id(adv_id)
        return adv.to_dict()

    async def get_all_advs(self) -> list[dict[str, str | int]]:
        async with self.session as session:
            advs = await session.execute(select(Advertisement))
            advs = advs.scalars().all()
            return [adv.to_dict() for adv in advs]

    async def update_adv(self, adv_id: int, validated_data: dict[str, str]) -> dict[str, str | int]:
        adv = await self.get_adv_instance_by_id(adv_id)
        async with self.session as session:
            for key, value in validated_data.items():
                if value is not None:
                    setattr(adv, key, value)
            await session.merge(adv)
            await session.commit()
            return adv.to_dict()

    async def delete_adv(self, adv_id: int) -> dict[str, int]:
        async with self.session as session:
            result = await session.execute(delete(Advertisement).where(Advertisement.id == adv_id))
            if result.rowcount == 0:
                raise web.HTTPNotFound(reason="Advertisement not found", content_type="application/json")
            await session.commit()
            return {"deleted": adv_id}
