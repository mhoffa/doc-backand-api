from pydantic import BaseModel

from core.entities import EntityType


class AutoCompleteOut(BaseModel):
    label: str
    metadata: dict
    type: EntityType
