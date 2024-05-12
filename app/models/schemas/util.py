from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PlainSerializer
from typing_extensions import Annotated


def datetime_serializer(dt: datetime):
    return dt.isoformat()


CustomDateTime = Annotated[
    datetime,
    PlainSerializer(datetime_serializer),
    # https://github.com/pydantic/pydantic/discussions/7199
    # this makes the model_dump:
    # {'any_custom_datetime': '2024-05-12T02:14:29.447476+00:00'}
]


class PageParam(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10


class PageResponse(BaseModel):
    total: int
    size: int
    page: int
    total_pages: int


class PaginatedResponse[T](BaseModel):
    data: list[T]
    paging: PageResponse


if __name__ == "__main__":
    from datetime import timezone

    class ExampleModel(BaseModel):
        x: datetime

    class NewModel(BaseModel):
        x: CustomDateTime

    m = ExampleModel(x=datetime.now(timezone.utc))
    print(m.model_dump())
    m = NewModel(x=datetime.now(timezone.utc))
    print(m.model_dump())
    if m.x < datetime.now(timezone.utc):
        print("yo")
