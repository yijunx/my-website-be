from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str


class LoginSession(BaseModel):
    id: str
    user_id: str
    expires: datetime
