from flask import Blueprint, current_app, request

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User, UserGetParam, UserPatchPayload
from app.models.schemas.util import PaginatedResponse
from app.services.user import UserServiceInterface
from app.utils.db import get_db
from app.utils.idp_helper import get_user_from_id_token
from app.utils.openapi import openapi
from app.utils.process_response import create_response
from app.utils.request_helper import get_session_id_from_request
from app.utils.service_registration import ServiceEnum

bp = Blueprint("internal_user", __name__, url_prefix="/api/external_user/v1/users")


@bp.route("", methods=["GET"])
@openapi()
def get_users(query: UserGetParam, response: PaginatedResponse[User]):
    session_id = get_session_id_from_request(request=request)
    try:
        with get_db() as db:
            s: UserServiceInterface = current_app.config[ServiceEnum.USER_SERVICE](db)
            actor = s.authenticate(login_session_id=session_id)
            r = s.list_users(query_param=query, actor=actor)
        return create_response(response=r)
    except CustomError as e:
        return create_response(status_code=e.status_code, message=e.message)
