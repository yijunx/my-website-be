from flask import Blueprint, current_app, request
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_serializer

from app.models.schemas.user import User
class Post(BaseModel):
    name: str
    content: str
    creator: User
    created_at: datetime