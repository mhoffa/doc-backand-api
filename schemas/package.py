from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
)


class PackageBase(BaseModel):
    name: str
    operation_type: str = Field(alias='operationType')
    operation_group: str = Field(alias='operationGroup')
    division_name: str = Field(alias='division')
    branch_name: str = Field(alias='branch')
    district_name: str = Field(alias='district')
    company_name: str = Field(alias='company')


class PackageUpdate(PackageBase):
    pass


class Package(PackageBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

