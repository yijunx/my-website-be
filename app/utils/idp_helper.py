from typing import Protocol

import jwt

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User


class IdpIDTokenParser(Protocol):
    @staticmethod
    def parse(payload: dict) -> User: ...


class GCPIDTokenParser(IdpIDTokenParser):
    @staticmethod
    def parse(payload: dict) -> User:
        return User(**payload)


def get_parser(iss: str) -> IdpIDTokenParser:
    parser_dict = {"https://accounts.google.com": GCPIDTokenParser()}
    parser = parser_dict.get(iss, None)
    if parser is None:
        raise CustomError(status_code=400, message=f"{iss} not accepted for login yet")
    return parser


def get_user_from_id_token(token: str) -> User:
    payload = jwt.decode(token, options={"verify_signature": False})
    parser = get_parser(iss=payload["iss"])
    return parser.parse(payload=payload)
