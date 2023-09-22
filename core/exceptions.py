from fastapi import (
    status,
    HTTPException,
)


class IncorrectSortField(HTTPException):
    def __init__(self, field: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The sorting field: {field} contains errors'
        )
