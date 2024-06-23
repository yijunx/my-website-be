import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from myauth import Actor
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User, UserGetParam, UserRoleEnum, Wink
from app.models.schemas.util import PaginatedResponse
from app.models.sqlalchemy import UserORM
from app.repositories.util import translate_query_pagination
from app.utils.config import configurations


class UserRepoInterface(ABC):
    @abstractmethod
    def upsert_user(self, actor: Actor) -> User: ...
    @abstractmethod
    def get_user(self, user_id: str) -> User: ...
    @abstractmethod
    def list_users(self, param: UserGetParam) -> PaginatedResponse[User]: ...


class SqlAlchemyUserRepo(UserRepoInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_user(self, actor: Actor) -> Wink:
        """used by the login endpoint, login endpoint will get the
        id token from the idp. the frontend nextjs app should already
        verified the idtoken. thus the idtoken here must be legit.
        """
        db_user: UserORM = (
            self.db.query(UserORM).filter(UserORM.email == actor.email).first()
        )

        if db_user:
            role = db_user.role
            previous_login_at = db_user.last_login_at
            # update stuff
            db_user.last_login_at = datetime.now(timezone.utc)
            db_user.realm = actor.iss.split("/")[-1]
            print("db user exist!!")
        else:
            previous_login_at = None
            role = UserRoleEnum.reader
            db_user = UserORM(
                id=actor.id,
                name=actor.name,
                email=actor.email,
                role=role,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                last_login_at=datetime.now(timezone.utc),
                realm=actor.iss.split("/")[-1],
            )
            self.db.add(db_user)
            print("db user added!!")

        if actor.email == configurations.MASTER_ACC_EMAIL:
            role = UserRoleEnum.admin
        return Wink(
            last_login_at=previous_login_at, role=role, realm=actor.iss.split("/")[-1]
        )

    def get_user(self, user_id: str) -> User:
        db_user: UserORM = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if db_user:
            return User.model_validate(db_user, from_attributes=True)
        else:
            raise CustomError(status_code=404, message="User does not exist")

    def list_users(self, param: UserGetParam) -> PaginatedResponse[User]:
        query = self.db.query(UserORM)

        if param.email:
            # email for exact match..
            query = query.filter(UserORM.email == param.email)
        else:
            if param.name:
                query = query.filter(UserORM.name.ilike(f"%{param.name}%"))

        total = query.count()
        limit, offset, paging = translate_query_pagination(
            total=total, query_param=param
        )
        db_items = query.limit(limit).offset(offset)

        return PaginatedResponse[User](
            data=[User.model_validate(x, from_attributes=True) for x in db_items],
            paging=paging,
        )
