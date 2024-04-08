from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.settings import app_settings, service_postgres_settings

if app_settings.mode == "TEST":
    DATABASE_URL = service_postgres_settings.test_postgresql_url
    DATABASE_ARGS = {"poolclass": NullPool}
else:
    DATABASE_URL = service_postgres_settings.postgresql_url
    DATABASE_ARGS = {}

async_engine = create_async_engine(DATABASE_URL, **DATABASE_ARGS)
async_session_maker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
