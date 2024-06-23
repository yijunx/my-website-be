from typing import Protocol

import jwt

from app.models.exceptions.base import CustomError

# from app.models.schemas.user import UserFromIDToken


# class IdpIDTokenParser(Protocol):
#     @staticmethod
#     def parse(payload: dict) -> UserFromIDToken: ...


# class GCPIDTokenParser(IdpIDTokenParser):
#     @staticmethod
#     def parse(payload: dict) -> UserFromIDToken:
#         return UserFromIDToken(
#             name=payload["name"],
#             first_name=payload["given_name"],
#             last_name=payload["family_name"],
#             provider="google",
#             provider_account_id=payload["sub"],
#             email=payload["email"],
#         )


# class MockIDTokenParser(IdpIDTokenParser):
#     @staticmethod
#     def parse(payload: dict) -> UserFromIDToken:
#         return UserFromIDToken(
#             name=payload["name"],
#             first_name=payload["given_name"],
#             last_name=payload["family_name"],
#             provider="geegle",
#             provider_account_id=payload["sub"],
#             email=payload["email"],
#         )


# def get_parser(iss: str) -> IdpIDTokenParser:
#     parser_dict = {
#         "https://accounts.geegle.com": MockIDTokenParser(),
#         "https://accounts.google.com": GCPIDTokenParser(),
#     }
#     parser = parser_dict.get(iss, None)
#     if parser is None:
#         raise CustomError(status_code=400, message=f"{iss} not accepted for login yet")
#     return parser


# def get_user_from_id_token(token: str) -> UserFromIDToken:
#     payload = jwt.decode(token, options={"verify_signature": False})
#     parser = get_parser(iss=payload["iss"])
#     return parser.parse(payload=payload)
