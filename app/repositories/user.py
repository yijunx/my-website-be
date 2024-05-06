import uuid
from datetime import datetime, timezone

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.schemas.user import User
from app.models.sqlalchemy import (AccountORM, SessionORM, UserORM,
                                   VerificationTokenORM)


def upsert_user(db: Session, user: User) -> UserORM:
    """used by the login endpoint, login endpoint will get the
    id token from the idp. the frontend nextjs app should already
    verified the idtoken. thus the idtoken here must be legit.
    """
    db_user: UserORM = db.query(UserORM).filter(UserORM.id == user.id).first()

    if db_user:
        # if the db_user exists
        # do the modification if needed
        pass
    else:
        db_user = UserORM(
            id=str(uuid.uuid4()),
            name=user.name,
            email=user.email,
        )
        db.add(db_user)
    return db_user


def get_session(db: Session, session_id: str) -> SessionORM: ...
