import jwt
import pytest
from app.models.schemas.user import UserFromIDToken
from app.utils.idp_helper import get_user_from_id_token


@pytest.fixture
def fake_gcp_idtoken() -> str:
    payload = {
        "iss": "https://accounts.google.com",
        "azp": "xxxx.apps.googleusercontent.com",
        "aud": "xxxx.apps.googleusercontent.com",
        "sub": "456781231",
        "hd": "yijun.corp",
        "email": "yijun@corp.io",
        "email_verified": True,
        "at_hash": "somehashhere",
        "name": "Yijun Xu",
        "picture": "https://lh3.googleusercontent.com/a/lalalahaha",
        "given_name": "Yijun",
        "family_name": "Xu",
        "iat": 1714984269,
        "exp": 1714987869,
    }
    return jwt.encode(payload=payload, key="verysecure")



@pytest.fixture
def user_from_id_token(fake_gcp_idtoken) -> UserFromIDToken:
    return get_user_from_id_token(fake_gcp_idtoken)
