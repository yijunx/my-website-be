import jwt
import pytest

from app.main import create_app
from app.models.schemas.user import UserFromIDToken
from app.services.user import MockUserService
from app.utils.idp_helper import get_user_from_id_token


@pytest.fixture
def user_id():
    return "zxcv"


@pytest.fixture
def login_session_id():
    return "1234"


@pytest.fixture
def client(user_id: str, login_session_id: str):
    app = create_app(
        user_service=MockUserService(login_session_id=login_session_id, user_id=user_id)
    )
    with app.test_client() as c:
        yield c


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


@pytest.fixture
def headers_with_id_token(fake_gcp_idtoken):
    return {"Authorization": f"Bearer {fake_gcp_idtoken}"}
