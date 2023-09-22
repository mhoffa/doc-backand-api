import logging

from pydantic_settings import BaseSettings
from pydantic import (
    SecretStr,
    PostgresDsn,
    field_validator,
)


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    ALLOW_REDIRECT_SLASHES: bool = False

    DATETIME_FORMAT: str = '%d.%m.%Y %H:%M:%S'

    LOGGING_LEVEL: int = logging.INFO
    LOGGING_NAME: str = 'doc-backend-api'
    LOGGING_FORMAT: str = 'rich_tb'

    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_SERVER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_LOCALE: str = 'en_US.utf8'
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator('SQLALCHEMY_DATABASE_URI')
    def assemble_db_connection(cls, v: str | None, values: dict[str, any]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.data.get('POSTGRES_USER'),
            password=values.data.get('POSTGRES_PASSWORD').get_secret_value(),
            host=values.data.get('POSTGRES_SERVER'),
            port=values.data.get('POSTGRES_PORT'),
            path=f"{values.data.get('POSTGRES_DB')}",
        )

    class Config:
        env_file = '.env'
        case_sensitive = False
        env_file_encoding = 'utf-8'
        secrets_dir = 'secrets'


settings = Settings()
