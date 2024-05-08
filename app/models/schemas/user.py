from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_serializer


class UserRoleEnum(str, Enum):
    reader = "reader"
    editor = "editor"
    admin = "admin"


class UserFromIDToken(BaseModel):
    name: str
    email: str
    first_name: str
    last_name: str
    provider: str
    provider_account_id: str


class LoginSession(BaseModel):
    id: str
    user_id: str
    expires: datetime

    @field_serializer("expires")
    def serialize_dt(self, dt: datetime):
        iso_datetime = dt.isoformat()
        if not iso_datetime.endswith("+00:00"):
            iso_datetime = iso_datetime + "+00:00"
        return iso_datetime


class User(BaseModel):
    id: str
    name: str
    email: str
    role: UserRoleEnum
    created_at: datetime
    updated_at: datetime
