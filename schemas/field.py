from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
)


class FieldBase(BaseModel):
    description: str = Field(alias='label')
    value: str | None = None
    value_box: list[float] | None = None


class FieldInDB(FieldBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
