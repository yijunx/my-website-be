import os
import re

from flask import Request
from myauth import Actor, AuthSettings, authenticate_token

from app.models.exceptions.base import CustomError
from app.utils.config import configurations


def get_token_from_header(auth_header: str) -> str:
    m = re.match(r"bearer (.+)", auth_header, re.IGNORECASE)
    if m is None:
        raise Exception("invalid authorization type")
    token = m.group(1)
    return token


def get_token_from_cookie(request: Request):
    token: str = request.cookies.get("token", None)
    return token


def get_session_id_from_request(request: Request):
    session_id: str = request.headers.get("X-Session-Id", None)
    if session_id is None:
        raise CustomError(status_code=401, message="unauthorized")
    return session_id


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


def get_actor_from_request(request: Request) -> Actor:

    token = get_token_from_request(request=request, check_token_from_cookie=False)
    auth_settings = AuthSettings(**configurations.model_dump())
    verify_signature = True
    if os.getenv("ENV"):
        verify_signature = True
    else:
        verify_signature = False

    try:
        return authenticate_token(
            token=token, config=auth_settings, verify_signature=verify_signature
        )
    except Exception as e:
        print(e)
        raise CustomError(401, "Authentication failed.")
