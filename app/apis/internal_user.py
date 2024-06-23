from flask import Blueprint, current_app, request

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User, Wink
from app.services.user import UserServiceInterface
from app.utils.db import get_db
from app.utils.openapi import openapi
from app.utils.process_response import create_response
from app.utils.request_helper import get_actor_from_request
from app.utils.service_registration import ServiceEnum

bp = Blueprint("internal_user", __name__, url_prefix="/apis/internal_user/v1")


@bp.route("/wink", methods=["POST"])
@openapi()
def login(response: Wink):
    """frontend pass the access token at login
    backend create the user and remembers the last login
    """
    try:
        actor = get_actor_from_request(request=request)
        with get_db() as db:
            # here we start a unit of work!
            s: UserServiceInterface = current_app.config[ServiceEnum.USER_SERVICE](db)
            r = s.wink_at_login(actor=actor)
        return create_response(response=r)
    except CustomError as e:
        return create_response(status_code=e.status_code, message=e.message)
