from app.models.schemas.user import UserFromIDToken
from app.repositories.user import SqlAlchemyUserRepo
from app.services.user import UserService, UserGetParam, User, UserRoleEnum
from app.utils.db import get_db


def test_login_and_authenticate(user_from_id_token: UserFromIDToken):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        session = s.login(user_from_id_token=user_from_id_token)
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        user = s.authenticate(session.id)
    assert user.name == user_from_id_token.name
    assert user.role == "reader"


def test_admin_list_users():
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
