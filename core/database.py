from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Base
from core.settings import Settings

PG_DSN = (
    f"postgresql+asyncpg://"
    f"{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}@"
    f"{Settings.POSTGRES_HOST}:{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}"
)


engine = create_async_engine(PG_DSN)
DbSession = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_orm() -> None:
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


async def close_orm() -> None:
    await engine.dispose()
