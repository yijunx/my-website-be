from enum import Enum

from pydantic import BaseModel
from app.models.schemas.util import CustomDateTime


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
    expires: CustomDateTime


class User(BaseModel):
    id: str
    name: str
    email: str
    role: UserRoleEnum
    created_at: CustomDateTime
    updated_at: CustomDateTime


class UserPatch(BaseModel):
    role: UserRoleEnum
