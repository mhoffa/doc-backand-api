import logging

from rich.logging import RichHandler

from .config import settings


logging.basicConfig(
    level=settings.LOGGING_LEVEL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger(settings.LOGGING_NAME)
