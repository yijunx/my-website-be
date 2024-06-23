from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models.schemas.util import CustomDateTime, PageParam, PageResponse


class UserRoleEnum(str, Enum):
    reader = "reader"
    editor = "editor"
    admin = "admin"


class User(BaseModel):
    id: str
    name: str
    email: str
    role: UserRoleEnum
    created_at: CustomDateTime
    updated_at: CustomDateTime


class UserPatchPayload(BaseModel):
    role: UserRoleEnum


class UserGetParam(PageParam):
    name: Optional[str] = None
    email: Optional[str] = None


class Wink(BaseModel):
    last_login_at: Optional[CustomDateTime] = None
    role: UserRoleEnum
    realm: str
