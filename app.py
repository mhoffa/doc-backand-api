import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import log, settings
from endpoints.v1.api import api_router


app = FastAPI(
    version='0.1.3',
    title='Doc-Backend-API',
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    log.info('Starting DOC-Backend-API')
    uvicorn.run(app, host=settings.UVICORN_HOST, port=settings.UVICORN_PORT)
