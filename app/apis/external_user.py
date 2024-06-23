from flask import Blueprint, current_app, request

from app.models.exceptions.base import CustomError
from app.models.schemas.user import User, UserGetParam, UserPatchPayload
from app.models.schemas.util import PaginatedResponse
from app.services.user import UserServiceInterface
from app.utils.db import get_db
from app.utils.openapi import openapi
from app.utils.process_response import create_response
from app.utils.request_helper import get_actor_from_request
from app.utils.service_registration import ServiceEnum

bp = Blueprint("external_user", __name__, url_prefix="/apis/my-website-be/v1/users")


@bp.route("/<user_id>/profile", methods=["GET"])
@openapi()
def profile(user_id: str):
    """upon user login, always wink pls (at client component)"""
    try:
        actor = get_actor_from_request(request=request)
        with get_db() as db:
            user_service: UserServiceInterface = current_app.config[
                ServiceEnum.USER_SERVICE
            ](db)
            r = user_service.get_user_profile(user_id=user_id, actor=actor)
        return create_response(response=r)
    except CustomError as e:
        return create_response(status_code=e.status_code, message=e.message)
