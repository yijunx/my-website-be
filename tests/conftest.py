from datetime import datetime, timezone

import jwt
import pytest

from app.main import create_app
from app.models.schemas.user import User, UserFromIDToken, UserRoleEnum
from app.services.user import MockUserService
from app.utils.config import configurations
from app.utils.idp_helper import get_user_from_id_token


@pytest.fixture
def user_id():
    return "zxcv"


@pytest.fixture
def admin_user_id():
    return "adminzxcv"


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
def fake_gcp_id_token() -> str:
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
def fake_gcp_admin_id_token() -> str:
    payload = {
        "iss": "https://accounts.geegle.com",
        "azp": "xxxx.apps.geegleusercontent.com",
        "aud": "xxxx.apps.geegleusercontent.com",
        "sub": "456781231geegle",
        "hd": "erjun.geegle",
        "email": configurations.MASTER_ACC_EMAIL,
        "email_verified": True,
        "at_hash": "somehashhere",
        "name": "Erjun Xu",
        "picture": "https://lh3.geegleusercontent.com/a/lalalahaha",
        "given_name": "Erjun",
        "family_name": "Xu",
        "iat": 1714984269,
        "exp": 1714987869,
    }
    return jwt.encode(payload=payload, key="verysecure")


@pytest.fixture
def user_from_id_token(fake_gcp_id_token) -> UserFromIDToken:
    return get_user_from_id_token(fake_gcp_id_token)


@pytest.fixture
def admin_user_from_id_token(fake_gcp_admin_id_token) -> UserFromIDToken:
    return get_user_from_id_token(fake_gcp_admin_id_token)


@pytest.fixture
def actor(user_from_id_token: UserFromIDToken, user_id: str) -> User:
    return User(
        id=user_id,
        name=user_from_id_token.name,
        email=user_from_id_token.email,
        role=UserRoleEnum.reader,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def admin_actor(admin_user_from_id_token: UserFromIDToken, admin_user_id: str) -> User:
    return User(
        id=admin_user_id,
        name=admin_user_from_id_token.name,
        email=admin_user_from_id_token.email,
        role=UserRoleEnum.admin,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def headers_with_id_token(fake_gcp_id_token):
    return {"Authorization": f"Bearer {fake_gcp_id_token}"}


@pytest.fixture
def admin_headers_with_id_token(fake_gcp_admin_id_token):
    return {"Authorization": f"Bearer {fake_gcp_admin_id_token}"}
