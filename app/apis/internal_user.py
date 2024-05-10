from flask import Blueprint, current_app, request

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User
from app.services.user import UserServiceInterface
from app.utils.db import get_db
from app.utils.idp_helper import get_user_from_id_token
from app.utils.openapi import validate
from app.utils.process_response import create_response
from app.utils.request_helper import get_token_from_request
from app.utils.service_registration import ServiceEnum

bp = Blueprint("internal_user", __name__, url_prefix="/api/internal_user/v1")


@bp.route("/login", methods=["POST"])
def login():
    user = get_user_from_id_token(get_token_from_request(request))
    try:
        with get_db() as db:
            # here we start a unit of work!
            s: UserServiceInterface = current_app.config[ServiceEnum.USER_SERVICE](db)
            p = s.login(user=user)
        return create_response(response=p)
    except CustomError as e:
        return create_response(status_code=e.status_code, message=e.message)


@bp.route("/sessions/<session_id>", methods=["GET"])
@validate()
def get_latest_alive_session(body: User, query: User, response: User):
    # email in the query parameter
    return {"upu": 1}, 200
