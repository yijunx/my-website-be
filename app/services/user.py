import app.repositories.user as UserRepo
from app.models.schemas.user import LoginSession, UserFromIDToken, User
from app.utils.config import configurations
from app.utils.db import get_db


def login(user: UserFromIDToken) -> LoginSession:
    with get_db() as db:
        db_user = UserRepo.upsert_user(db=db, user_from_id_token=user)
        _ = UserRepo.upsert_account(db=db, user_from_id_token=user, user_id=db_user.id)
        db_login_session = UserRepo.create_login_session(
            db=db,
            user_id=db_user.id,
            login_session_lasts_in_seconds=configurations.LOGIN_SESSION_LASTS_IN_SECONDS,
        )
        login_session = LoginSession.model_validate(db_login_session, from_attributes=True)
    return login_session


def logout(): ...


def authenticate(login_session_id: str) -> User:
    with get_db() as db:
        db_login_session = UserRepo.get_session(db=db, login_session_id=login_session_id)
        db_user = UserRepo.get_user(db=db, user_id=db_login_session.user_id)
        user = User.model_validate(db_user, from_attributes=True)
    return user
        
        


    



def remove_user():
    ...
