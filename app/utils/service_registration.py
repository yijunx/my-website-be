from enum import Enum

from flask import Flask
from sqlalchemy.orm import Session

from app.repositories.user import SqlAlchemyUserRepo, UserRepoInterface
from app.services.user import UserService, UserServiceInterface

# class ServiceRegistration:
#     def __init__(self, user_service: UserServiceInterface) -> None:
#         self.user_service = user_service


class ServiceEnum(str, Enum):
    USER_SERVICE = "USER_SERVICE"
    POST_SERVICE = "POST_SERVICE"
    FILE_SERVICE = "FILE_SERVICE"


def register_services_func(
    app: Flask, user_service: UserServiceInterface | None
) -> None:
    """here you can replace any service with service for test!"""
    def f(session: Session) -> UserServiceInterface:
        # user service
        if user_service:
            s = user_service
        else:  # our default
            s = UserService(user_repo=SqlAlchemyUserRepo(db=session))
        return s

    app.config[ServiceEnum.USER_SERVICE] = f
