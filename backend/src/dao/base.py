from fastapi import HTTPException
from functools import wraps

from backend.database import async_session_maker
from pydantic import BaseModel

from sqlalchemy import select, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession




class BaseDAO:
    model = None

    def with_session(func):
        @wraps(func)
        async def wrapper(cls, session=None, *args, **kwargs):
            print(f"Function: {func.__qualname__}, session before check: {session}")
            if session is None:
                async with async_session_maker() as session:
                    print("Created new session:", session)
                    return await func(cls, session, *args, **kwargs)
            return await func(cls, session, *args, **kwargs)
        return wrapper

    @classmethod
    @with_session
    async def create(cls, session: AsyncSession, data: BaseModel):
        object = cls.model(**data.model_dump())
        session.add(object)
        await session.commit()
        return object
    
    @classmethod
    @with_session
    async def create_many(cls, session: AsyncSession, data: list[BaseModel]):
        query = insert(cls.model).values(
            [
                object.model_dump() for object in data
            ]
        ).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().all()
    
    @classmethod
    @with_session
    async def find_all(cls, session: AsyncSession, **kwargs):
        query = select(cls.model).filter_by(**kwargs).order_by(cls.model.id)
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    @with_session
    async def find_by_id(cls, session: AsyncSession, model_id):
        query = select(cls.model).where(cls.model.id==model_id)
        result = await session.execute(query)
        if not (object := result.scalar_one_or_none()):
            raise HTTPException(status_code=404, detail='Object is not found')
        return object
    
    @classmethod
    @with_session
    async def find_all_by_id(cls, session: AsyncSession, model_ids):
        query = select(cls.model).where(cls.model.id.in_(model_ids))
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    @with_session
    async def update(cls, session: AsyncSession, object_id,
                     updated_data, partial: bool):
        object = await cls.find_by_id(session, object_id)
        
        updated = updated_data.model_dump(exclude_unset=partial)
        for key, value in updated.items():
            setattr(object, key, value)
        
        await session.commit()
        return object
        
    @classmethod
    @with_session
    async def destroy(cls, session: AsyncSession, object_id):
        object = await cls.find_by_id(session, object_id)
        
        query = delete(cls.model).where(cls.model.id == object.id)
        await session.execute(query)
        await session.commit()

        return {"detail": "Object deleted successfully"}
    
    @classmethod
    @with_session
    async def count(cls, session: AsyncSession):
        query = (
            select(func.count('*')).select_from(cls.model)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
