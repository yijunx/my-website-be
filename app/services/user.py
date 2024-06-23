from abc import ABC, abstractmethod
from datetime import datetime, timezone

from myauth import Actor

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User, UserGetParam, UserRoleEnum, Wink
from app.models.schemas.util import PageResponse, PaginatedResponse
from app.repositories.user import UserRepoInterface


class UserServiceInterface(ABC):
    @abstractmethod
    def wink_at_login(self, actor: Actor) -> Wink:
        """from the id token from idp, return a login session"""

    @abstractmethod
    def get_user_profile(self, user_id: str, actor: Actor) -> User:
        """check if the login session is still valid"""


class MockUserService(UserServiceInterface):
    def __init__(self, wink: Wink, user_id: str) -> None:
        self.wink = wink
        self.user = User(
            id=user_id,
            name="user_name",
            email="user_email",
            role="reader",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def wink_at_login(self, actor: Actor) -> Wink:
        return self.wink

    def get_user_profile(self, user_id: str, actor: Actor) -> User:
        return self.user


class UserService(UserServiceInterface):
    def __init__(self, user_repo: UserRepoInterface) -> None:
        self.user_repo = user_repo

    def wink_at_login(self, actor: Actor) -> Wink:
        return self.user_repo.upsert_user(actor=actor)

    def get_user_profile(self, user_id: str, actor: Actor) -> User:
        user = self.user_repo.get_user(user_id=user_id)
        print(user)
        if user.role == UserRoleEnum.admin:
            return user
        else:
            if user.id == actor.id:
                return user
            else:
                raise CustomError(
                    status_code=403, message="You cannot get others profile"
                )

    def list_users(
        self, query_param: UserGetParam, actor: User
    ) -> PaginatedResponse[User]:
        if actor.role != UserRoleEnum.admin:
            raise CustomError(status_code=403, message="unauthorized")
        return self.user_repo.list_users(param=query_param)
