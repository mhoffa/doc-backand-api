from typing import Annotated
from json import JSONDecodeError

from fastapi import (
    status,
    Query,
    Depends,
    Request,
    APIRouter,
    HTTPException,
)

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas

from db import get_session_db
from core.entities import AutoCompleteStrategies

from core.utils import delete_duplicate_from_list_entities


router = APIRouter()

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MIN_QUERY_LENGTH = 3


@router.get('/', response_model=list[schemas.Document])
async def get_documents(
        request: Request,
        skip: int = Query(DEFAULT_SKIP, description='Number of items to skip'),
        limit: int = Query(DEFAULT_LIMIT, description='Maximum number of items to return'),
        session: AsyncSession = Depends(get_session_db),
):
    try:
        json_body = await request.json()
        queries = schemas.DocumentQuery(**json_body)
    except (JSONDecodeError, ValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid JSON body!')

    documents = await crud.document.get_list(
        session,
        skip=skip,
        limit=limit,
        filters=queries.filters,
    )

    return documents


@router.get('/search', response_model=list[schemas.AutoCompleteOut])
async def search(
        q: Annotated[str, Query(min_length=MIN_QUERY_LENGTH)],
        limit: int = 10,
        session: AsyncSession = Depends(get_session_db),
):
    if not q:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Param q is empty!')

    documents = await crud.document.search(session, limit=limit, q=q)

    result = [AutoCompleteStrategies.get(doc, matched_field) for doc, matched_field in documents]

    return delete_duplicate_from_list_entities(result)
