from datetime import datetime
from typing_extensions import Annotated
from pydantic import PlainSerializer


CustomDateTime = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.isoformat()),
    # this makes the model_dump:
    # {'any_custom_datetime': '2024-05-12T02:14:29.447476+00:00'}
]

if __name__ == "__main__":
    from pydantic import BaseModel
    from datetime import timezone


    class ExampleModel(BaseModel):
        x: datetime
    class NewModel(BaseModel):
        x: CustomDateTime

    m = ExampleModel(x=datetime.now(timezone.utc))
    print(m.model_dump())
    m = NewModel(x=datetime.now(timezone.utc))
    print(m.model_dump())