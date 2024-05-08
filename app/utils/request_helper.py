import re

from flask import Request

from app.models.exceptions.base import CustomError


def get_token_from_header(auth_header: str) -> str:
    m = re.match(r"bearer (.+)", auth_header, re.IGNORECASE)
    if m is None:
        raise Exception("invalid authorization type")
    token = m.group(1)
    return token


def get_token_from_cookie(request: Request):
    token: str = request.cookies.get("token", None)
    return token


def get_auth_header(request: Request) -> str:
    try:
        auth_header = request.headers["authorization"]
        return auth_header
    except KeyError:
        raise Exception("Unable to head authorization header")


def get_token_from_request(
    request: Request, check_token_from_cookie: bool = False
) -> str:
    token = None
    if check_token_from_cookie:
        token = get_token_from_cookie(request=request)
    if token is None:
        try:
            auth_header = get_auth_header(request=request)
            token = get_token_from_header(auth_header=auth_header)
        except Exception as e:
            raise CustomError(401, "failed to get token")

    return token


def request_validation(request: Request, params=None, body=None): ...


def request_validation_with_authorization(request: Request, params=None, body=None): ...