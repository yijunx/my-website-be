from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.models.exceptions.base import CustomError
from app.models.schemas.user import (
    LoginSession,
    User,
    UserFromIDToken,
    UserGetParam,
    UserRoleEnum,
)
from app.models.schemas.util import PageResponse, PaginatedResponse
from app.repositories.user import UserRepoInterface
from app.utils.config import configurations


class UserServiceInterface(ABC):
    @abstractmethod
    def login(self, user_from_id_token: UserFromIDToken) -> LoginSession:
        """from the id token from idp, return a login session"""

    @abstractmethod
    def authenticate(self, login_session_id: str) -> User:
        """check if the login session is still valid"""

    @abstractmethod
    def list_users(
        self, query_param: UserGetParam, actor: User
    ) -> PaginatedResponse[User]:
        """just list users"""


class MockUserService(UserServiceInterface):
    def __init__(self, login_session_id: str, user_id: str) -> None:
        self.login_session_id = login_session_id
        self.user_id = user_id
        self.user = User(
            id=self.user_id,
            name="user_name",
            email="user_email",
            role="reader",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def login(self, user_from_id_token: UserFromIDToken) -> LoginSession:
        return LoginSession(
            id=self.login_session_id, user_id=self.user_id, expires=datetime.now()
        )

    def authenticate(self, login_session_id: str) -> User:
        return self.user

    def list_users(
        self, query_param: UserGetParam, actor: User
    ) -> PaginatedResponse[User]:
        return PaginatedResponse[User](
            data=[self.user],
            paging=PageResponse(total=1, size=1, page=1, total_pages=1),
        )


class UserService(UserServiceInterface):
    def __init__(self, user_repo: UserRepoInterface) -> None:
        self.user_repo = user_repo

    def login(self, user_from_id_token: UserFromIDToken) -> LoginSession:
        user = self.user_repo.upsert_user(user_from_id_token=user_from_id_token)
        _ = self.user_repo.upsert_account(
            user_from_id_token=user_from_id_token, user_id=user.id
        )
        return self.user_repo.create_login_session(
            user_id=user.id,
            login_session_lasts_in_seconds=configurations.LOGIN_SESSION_LASTS_IN_SECONDS,
        )

    def authenticate(self, login_session_id: str) -> User:
        login_session = self.user_repo.get_login_session(
            login_session_id=login_session_id
        )
        # the info comes back from db does not have datetime!!!
        # because we want the db to save as utc, but we want it timezone unaware!!
        # so that we save the time to setup db with timezone...
        if login_session.expires.astimezone(timezone.utc) < datetime.now(timezone.utc):
            raise CustomError(status_code=401, message="Session expired")
        return self.user_repo.get_user(user_id=login_session.user_id)

    def list_users(
        self, query_param: UserGetParam, actor: User
    ) -> PaginatedResponse[User]:
        if actor.role != UserRoleEnum.admin:
            raise CustomError(status_code=403, message="unauthorized")
        return self.user_repo.list_users(param=query_param)
