import pytest

from app.models.exceptions.base import CustomError
from app.models.schemas.user import UserFromIDToken
from app.repositories.user import SqlAlchemyUserRepo
from app.services.user import User, UserGetParam, UserRoleEnum, UserService
from app.utils.db import get_db


def test_login_and_authenticate(user_from_id_token: UserFromIDToken):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        session = s.login(user_from_id_token=user_from_id_token)
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        user = s.authenticate(session.id)
    assert user.name == user_from_id_token.name
    assert user.role == UserRoleEnum.reader


def test_admin_login_and_authenticate(admin_user_from_id_token: UserFromIDToken):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        session = s.login(user_from_id_token=admin_user_from_id_token)
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        user = s.authenticate(session.id)
    assert user.name == admin_user_from_id_token.name
    assert user.role == UserRoleEnum.admin


def test_admin_list_users(admin_actor: User):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        r = s.list_users(query_param=UserGetParam(), actor=admin_actor)
    assert r.data is not None
    assert r.paging.page == 1


def test_user_list_users(actor: User):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        with pytest.raises(CustomError):
            s.list_users(query_param=UserGetParam(), actor=actor)
