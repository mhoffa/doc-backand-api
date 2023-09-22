from typing import Sequence

from sqlalchemy import (
    or_,
    and_,
    case,
    select,
)
from sqlalchemy.sql import (
    asc,
    desc,
    collate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    load_only,
    selectinload,
)

import models

from core import settings
from .base import CrudBase
from schemas import DocumentUpdate
from core.utils import (
    pretty_result,
    get_value_from_dict_by_partial_key,
)
from core.entities import (
    CodeErrors,
    DOCUMENT_STATUS,
    DOCUMENT_PRIORITY,
)


class CrudDocument(CrudBase[models.Document, DocumentUpdate]):
    PACKAGE_FIELDS: dict = {f.name: f for f in models.Package.__table__.columns}
    DOCUMENT_FIELDS: dict = {f.name: f for f in models.Document.__table__.columns}

    ALLOWED_FILTER_FIELDS: list = [
        models.Document.name,
        models.Document.document_type,
        models.Package.name,
        models.Package.operation_type,
        models.Package.operation_group,
    ]

    def __init__(self, model: any):
        super().__init__(model)

    async def get(self, session: AsyncSession, id: any) -> dict:
        query = (
            select(models.Document)
            .filter_by(id=id)
            .options(
                selectinload(models.Document.package),
                selectinload(models.Document.pages).selectinload(models.Page.fields),
            )
            .join(models.Package)
        )

        result = await session.execute(query)
        document = result.scalar_one_or_none()

        if not document:
            return pretty_result(CodeErrors.DB_ERROR.value, f'{self.model.__name__} not found by id: {id}')
        return pretty_result(CodeErrors.OK.value, data=document)

    def _get_document_filters(self, filters: list[dict]) -> list:
        document_filters = []

        for filt in filters:
            conditions = []
            for attr, value in filt.items():
                document_attr = self.DOCUMENT_FIELDS.get(attr)
                package_attr = self.PACKAGE_FIELDS.get(attr)

                if document_attr is not None:
                    conditions.append(document_attr == value)
                elif package_attr is not None:
                    conditions.append(package_attr == value)
            document_filters.append(and_(*conditions))

        return document_filters

    def _get_values_priority_and_status_if_exists(self, value: str) -> tuple[int, int]:
        status = get_value_from_dict_by_partial_key(DOCUMENT_STATUS, value)
        priority = get_value_from_dict_by_partial_key(DOCUMENT_PRIORITY, value)
        return priority, status

    async def get_list(
            self,
            session: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            **kwargs,
    ) -> Sequence[models.Document]:
        filters = self._get_document_filters(kwargs.get('filters', []))

        query = (
            select(models.Document)
            .where(or_(*filters))
            .options(
                selectinload(models.Document.package),
                selectinload(models.Document.pages).selectinload(models.Page.fields),
            )
            .join(models.Package)
            .offset(skip)
            .limit(limit)
        )

        result = await session.execute(query)
        return result.scalars().all()

    def _get_filters(self, value: str):
        filters = []

        for field in self.ALLOWED_FILTER_FIELDS:
            filters.append(
                collate(field, settings.POSTGRES_LOCALE).ilike(f'{value}%')
            )

        return or_(*filters)

    def _get_case_expression(self, value: str):
        expressions = []
        for field in self.ALLOWED_FILTER_FIELDS:
            expressions.append(
                (collate(field, settings.POSTGRES_LOCALE).ilike(f'{value}%'), field.name)
            )
        return case(*expressions, else_='unknown')

    async def search(self, session: AsyncSession, *, limit: int, q: str):
        case_expression = self._get_case_expression(q)

        query = (
            select(models.Document)
            .options(
                load_only(
                    models.Document.name,
                    models.Document.document_type,
                )
            )
            .options(
                selectinload(
                    models.Document.package
                ).load_only(
                    models.Package.name,
                    models.Package.operation_type,
                    models.Package.operation_group,
                )
            )
            .join(models.Document.package)
            .add_columns(
                case_expression.label('matched_field')
            )
            .filter(
                self._get_filters(q)
            )
            .limit(limit - 1)
        )

        documents = await session.execute(query)
        documents = documents.fetchall()

        priority, status = self._get_values_priority_and_status_if_exists(q)

        if priority:
            documents.insert(0, ({'priority': priority}, 'priority'))
        if status:
            documents.insert(0, ({'status': status}, 'status'))

        return documents


document = CrudDocument(models.Document)