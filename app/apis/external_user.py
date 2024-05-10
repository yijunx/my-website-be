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

bp = Blueprint("internal_user", __name__, url_prefix="/api/external_user/v1/users")


@bp.route("", methods=["POST"])
def create_user():
    return {"upu": 1}, 200


@bp.route("", methods=["GET"])
@validate()
def get_users():
    return {"upu": 1}, 200
