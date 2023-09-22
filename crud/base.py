from typing import (
    Type,
    Union,
    Generic,
    TypeVar,
)

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.base_class import Base
from core.utils import pretty_result
from core.entities import CodeErrors


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CrudBase(Generic[ModelType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def model_dump(self, data: dict | list | BaseModel, exclude_unset: bool = True) -> dict:
        if isinstance(data, (dict, list)):
            return data

        return data.model_dump(exclude_unset=exclude_unset)

    async def get(self, session: AsyncSession, id: any) -> dict:
        obj = await session.get(self.model, id)
        if not obj:
            return pretty_result(CodeErrors.DB_ERROR.value, f'{self.model.__name__} not found by id: {id}')
        return pretty_result(CodeErrors.OK.value, data=obj)

    async def get_all(self, session: AsyncSession, *, skip: int = 0, limit: int = 100):
        query = select(self.model).offset(skip).limit(limit)
        entries = await session.execute(query)
        return entries.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: dict) -> pretty_result:
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return pretty_result(CodeErrors.OK.value, data=db_obj)
        except IntegrityError:
            await db.rollback()
            return pretty_result(CodeErrors.DB_ERROR.value, 'Error when creating a new record in a table')

    async def update(
            self,
            session: AsyncSession,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, dict],
            set_commit: bool = True
    ) -> dict:
        obj_data = jsonable_encoder(db_obj)
        update_data = self.model_dump(obj_in)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if set_commit:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

        return pretty_result(CodeErrors.OK.value, data=db_obj)

    async def remove(self, session: AsyncSession, *, id: int) -> dict:
        obj = await session.get(self.model, id)
        if not obj:
            return pretty_result(CodeErrors.DB_ERROR.value, f'{self.model.__name__} not found by id: {id}')

        await session.delete(obj)
        await session.commit()
        return pretty_result(CodeErrors.OK.value, data=obj)
