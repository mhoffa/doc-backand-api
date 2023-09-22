from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core import settings


_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
)

async_session = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session_db() -> AsyncSession:
    async with async_session() as session:
        yield session
