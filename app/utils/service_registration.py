from enum import Enum

from flask import Flask

from app.repositories.user import SqlAlchemyUserRepo
from app.services.user import UserService, UserServiceInterface


class ServiceEnum(str, Enum):
    USER_SERVICE = "USER_SERVICE"
    AUTH_SERVICE = "AUTH_SERVICE"


def register_services_func(
    app: Flask,
    user_service: UserServiceInterface = None,
) -> None:
    """here you can replace any service with service for test!"""

    def f_user_service(session) -> UserServiceInterface:
        if user_service:
            return user_service
        else:  # our default
            return UserService(user_repo=SqlAlchemyUserRepo(db=session))

    app.config[ServiceEnum.USER_SERVICE] = f_user_service
