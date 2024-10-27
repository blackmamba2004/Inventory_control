from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


def with_session(func):
    @wraps(func)
    async def wrapper(cls, session=None, *args, **kwargs):
        if session is None:
            async with async_session_maker() as session:
                return await func(cls, session, *args, **kwargs)
        return await func(cls, session, *args, **kwargs)

    return wrapper


async def get_db():
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
