from datetime import datetime
from typing import Protocol

from app.models.schemas.user import LoginSession, User, UserFromIDToken
from app.repositories.user import UserRepoInterface
from app.utils.config import configurations


class UserServiceInterface(Protocol):
    def login(self, user: UserFromIDToken) -> LoginSession: ...
    def authenticate(self, login_session_id: str) -> User: ...


class MockUserService(UserServiceInterface):
    def __init__(self, login_session_id: str, user_id: str) -> None:
        self.login_session_id = login_session_id
        self.user_id = user_id

    def login(self, user: UserFromIDToken) -> LoginSession:
        return LoginSession(
            id=self.login_session_id, user_id=self.user_id, expires=datetime.now()
        )

    def authenticate(self, login_session_id: str) -> User:
        return User(
            id=self.user_id,
            name="user_name",
            email="user_email",
            role="reader",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


class UserService(UserServiceInterface):
    def __init__(self, user_repo: UserRepoInterface) -> None:
        self.user_repo = user_repo

    def login(self, user: UserFromIDToken) -> LoginSession:
        db_user = self.user_repo.upsert_user(user_from_id_token=user)
        _ = self.user_repo.upsert_account(user_from_id_token=user, user_id=db_user.id)
        db_login_session = self.user_repo.create_login_session(
            user_id=db_user.id,
            login_session_lasts_in_seconds=configurations.LOGIN_SESSION_LASTS_IN_SECONDS,
        )
        login_session = LoginSession.model_validate(
            db_login_session, from_attributes=True
        )
        return login_session

    def authenticate(self, login_session_id: str) -> User:
        db_login_session = self.user_repo.get_session(login_session_id=login_session_id)
        db_user = self.user_repo.get_user(user_id=db_login_session.user_id)
        user = User.model_validate(db_user, from_attributes=True)
        return user
