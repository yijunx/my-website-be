from flask import Blueprint, current_app, request

from app.models.exceptions.base import CustomError
from app.services.user import UserServiceInterface
from app.utils.db import get_db
from app.utils.idp_helper import get_user_from_id_token
from app.utils.process_response import create_response
from app.utils.request_helper import get_token_from_request
from app.utils.service_registration import ServiceEnum

bp = Blueprint("internal_user", __name__, url_prefix="/api/post-service/v1/posts")


@bp.route("/", methods=["POST"])
def add_post():
    ...