from pydantic import BaseModel

from app.models.schemas.util import CustomDateTime


class Post(BaseModel):
    name: str
    content: str
    created_by: str
    created_at: CustomDateTime
    updated_at: CustomDateTime
