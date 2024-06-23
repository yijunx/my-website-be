from datetime import datetime, timezone

import jwt
import pytest
from myauth import Actor, authenticate_token

from app.main import create_app
from app.models.schemas.user import UserRoleEnum, Wink
from app.services.user import MockUserService
from app.utils.config import configurations


@pytest.fixture
def user_id():
    return "zxcv"


@pytest.fixture
def admin_id():
    return "adminzxcv"


@pytest.fixture
def client(user_id: str):
    app = create_app(
        user_service=MockUserService(
            wink=Wink(last_login_at=None, role=UserRoleEnum.reader, realm="myrealm"),
            user_id=user_id,
        )
    )
    with app.test_client() as c:
        yield c


@pytest.fixture
def user_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "email": "yijun@corp.io",
        "preferred_username": "sanjun@corp.io",
        "name": "tom bar",
        "first_name": "tom",
        "last_name": "bar",
        "iss": "https://domain/realms/my-realm",
    }
    return jwt.encode(payload=payload, key="verysecure")


@pytest.fixture
def admin_access_token(admin_id: str) -> str:
    payload = {
        "sub": admin_id,
        "email": configurations.MASTER_ACC_EMAIL,
        "preferred_username": "erjun@corp.io",
        "name": "tom admin",
        "first_name": "tom",
        "last_name": "admin",
        "iss": "https://domain/realms/my-realm",
    }
    return jwt.encode(payload=payload, key="verysecure")


@pytest.fixture
def admin_actor(admin_access_token) -> Actor:
    return authenticate_token(
        token=admin_access_token, config=None, verify_signature=False
    )


@pytest.fixture
def user_actor(user_access_token):
    return authenticate_token(
        token=user_access_token, config=None, verify_signature=False
    )


@pytest.fixture
def user_headers(user_access_token):
    return {"Authorization": f"Bearer {user_access_token}"}


@pytest.fixture
def admin_headers(admin_access_token):
    return {"Authorization": f"Bearer {admin_access_token}"}
