from pydantic import BaseModel
from typing import Optional


class PaginatedQuery(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10


class PaginatedResponse(BaseModel):
    total: int
    size: int
    page: int
    total_pages: int