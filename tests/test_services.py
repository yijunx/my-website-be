import pytest
from myauth import Actor

from app.models.exceptions.base import CustomError
from app.repositories.user import SqlAlchemyUserRepo
from app.services.user import User, UserGetParam, UserRoleEnum, UserService
from app.utils.db import get_db


def test_wink_admin(admin_actor: Actor):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        r = s.wink_at_login(actor=admin_actor)
    assert r.role == UserRoleEnum.admin


def test_wink_admin_again(admin_actor: Actor):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        r = s.wink_at_login(actor=admin_actor)
    assert r.role == UserRoleEnum.admin
    assert r.last_login_at is not None


def test_wink_user(user_actor: Actor):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        r = s.wink_at_login(actor=user_actor)
    assert r.role == UserRoleEnum.reader


def test_user_get_user(user_id: str, user_actor: Actor):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        r = s.get_user_profile(user_id=user_id, actor=user_actor)
    assert r.id == user_actor.id


# def test_admin_list_users(admin_actor: User):
#     with get_db() as db:
#         s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
#         r = s.list_users(query_param=UserGetParam(), actor=admin_actor)
#     assert r.data is not None
#     assert r.paging.page == 1


# def test_user_list_users(user_actor: User):
#     with get_db() as db:
#         s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
#         with pytest.raises(CustomError):
#             s.list_users(query_param=UserGetParam(), actor=actor)
