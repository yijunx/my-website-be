from app.models.schemas.user import UserFromIDToken
from app.services.user import UserService
from app.utils.db import get_db
from app.repositories.user import SqlAlchemyUserRepo


def test_login_and_authenticate(user_from_id_token: UserFromIDToken):
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        session = s.login(user=user_from_id_token)
    with get_db() as db:
        s = UserService(user_repo=SqlAlchemyUserRepo(db=db))
        user = s.authenticate(session.id)
    assert user.name == user_from_id_token.name
    assert user.role == "reader"
