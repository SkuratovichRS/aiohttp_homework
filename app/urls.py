from aiohttp import web

from app.views import AdvertisementViewSet, CreateTokenView, CreateUserView

urls = [
    web.post("/api/v1/users", CreateUserView),
    web.post("/api/v1/token", CreateTokenView),
    web.post("/api/v1/advertisements", AdvertisementViewSet),
    web.get("/api/v1/advertisements", AdvertisementViewSet),
    web.get("/api/v1/advertisements/{id:\d+}", AdvertisementViewSet),
    web.patch("/api/v1/advertisements/{id:\d+}", AdvertisementViewSet),
    web.put("/api/v1/advertisements/{id:\d+}", AdvertisementViewSet),
    web.delete("/api/v1/advertisements/{id:\d+}", AdvertisementViewSet),
]
