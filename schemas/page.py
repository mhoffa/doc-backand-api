from pydantic import (
    BaseModel,
    ConfigDict,
)

from .field import FieldInDB


class PageBase(BaseModel):
    page_order: int | None = None


class PageUpdate(PageBase):
    pass


class Page(PageBase):
    id: int
    fields: list[FieldInDB] | None = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
