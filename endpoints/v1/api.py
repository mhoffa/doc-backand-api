from fastapi import APIRouter

from core import settings
from .document import router as documents_router


api_router = APIRouter(redirect_slashes=settings.ALLOW_REDIRECT_SLASHES)
api_router.include_router(documents_router, prefix='/documents', tags=['documents'])
