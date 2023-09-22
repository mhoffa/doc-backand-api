from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
    field_validator,
)

from .page import (
    Page,
    PageUpdate,
)
from .package import (
    Package,
    PackageUpdate,
)
from core.entities import PATTERN_SORT_FIELDS
from core.exceptions import IncorrectSortField


class DocumentBase(BaseModel):
    name: str
    document_type: str = Field(alias='type')
    created_at: int = Field(alias='createdAt')
    updated_at: int = Field(alias='updatedAt')
    priority: int | None = None
    status: int | None = None
    conf: float = Field(alias='percent')
    revision: bool


class DocumentUpdate(DocumentBase):
    package: PackageUpdate | None = None
    pages: list[PageUpdate] | None = None


class Document(DocumentBase):
    id: int
    package: Package | None = None
    pages: list[Page] | None = []

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class DocumentQuery(BaseModel):
    filters: list[dict] | None = []
    sorting: list[str] | None = []

    @field_validator('sorting')
    def check_sort_fields(cls, value: str) -> str:
        for field in value:
            if not PATTERN_SORT_FIELDS.match(field):
                raise IncorrectSortField(field=field)

        return value
