from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(3, description="Кол-во записей на странице", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]