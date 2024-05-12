import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.exceptions.base import CustomError
from app.models.schemas.user import (
    Account,
    LoginSession,
    User,
    UserFromIDToken,
    UserGetParam,
    UserPatchPayload,
    UserRoleEnum,
)
from app.models.schemas.util import PaginatedResponse
from app.models.sqlalchemy import (
    AccountORM,
    LoginSessionORM,
    UserORM,
    VerificationTokenORM,
)
from app.repositories.util import translate_query_pagination


class UserRepoInterface(ABC):
    @abstractmethod
    def upsert_user(self, user_from_id_token: UserFromIDToken) -> User: ...
    @abstractmethod
    def get_user(self, user_id: str) -> User: ...
    @abstractmethod
    def upsert_account(
        self, user_from_id_token: UserFromIDToken, user_id: str
    ) -> Account: ...
    @abstractmethod
    def create_login_session(
        self, user_id: str, login_session_lasts_in_seconds: int
    ) -> LoginSession: ...
    @abstractmethod
    def get_login_session(self, login_session_id: str) -> LoginSession: ...
    @abstractmethod
    def list_users(self, query: UserGetParam) -> PaginatedResponse[User]: ...


class SqlAlchemyUserRepo(UserRepoInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def upsert_user(self, user_from_id_token: UserFromIDToken) -> UserORM:
        """used by the login endpoint, login endpoint will get the
        id token from the idp. the frontend nextjs app should already
        verified the idtoken. thus the idtoken here must be legit.
        """
        db_user: UserORM = (
            self.db.query(UserORM)
            .filter(UserORM.email == user_from_id_token.email)
            .first()
        )

        if db_user:
            # if the db_user exists
            # do the modification if needed
            pass
        else:
            db_user = UserORM(
                id=str(uuid.uuid4()),
                name=user_from_id_token.name,
                email=user_from_id_token.email,
                role=UserRoleEnum.reader,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            self.db.add(db_user)
        return User.model_validate(db_user, from_attributes=True)

    def get_user(self, user_id: str) -> User:
        db_user: UserORM = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if db_user:
            return User.model_validate(db_user, from_attributes=True)
        else:
            CustomError(status_code=404, message="User does not exist")

    def upsert_account(
        self, user_from_id_token: UserFromIDToken, user_id: str
    ) -> AccountORM:

        db_account: AccountORM = (
            self.db.query(AccountORM)
            .filter(
                AccountORM.provider == user_from_id_token.provider,
                AccountORM.provider_account_id
                == user_from_id_token.provider_account_id,
            )
            .first()
        )

        if db_account:
            pass
        else:
            db_account = AccountORM(
                id=str(uuid.uuid4()),
                user_id=user_id,
                provider=user_from_id_token.provider,
                provider_account_id=user_from_id_token.provider_account_id,
            )
        return Account.model_validate(db_account, from_attributes=True)

    def create_login_session(
        self, user_id: str, login_session_lasts_in_seconds: int
    ) -> LoginSessionORM:
        db_login_session = LoginSessionORM(
            id=str(uuid.uuid4()),
            user_id=user_id,
            expires=datetime.now(timezone.utc)
            + timedelta(seconds=login_session_lasts_in_seconds),
        )
        self.db.add(db_login_session)
        return LoginSession.model_validate(db_login_session, from_attributes=True)

    def get_login_session(self, login_session_id: str) -> LoginSessionORM:
        """for check login status..."""
        db_login_session = (
            self.db.query(LoginSessionORM)
            .filter(LoginSessionORM.id == login_session_id)
            .first()
        )

        if db_login_session:
            return LoginSession.model_validate(db_login_session, from_attributes=True)
        else:
            raise CustomError(status_code=401, message="You did not login")

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
