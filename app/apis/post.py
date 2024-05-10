# this is the resources
# suppose only some kind of user can create post, and kind of user
# can only read posts
from flask import Blueprint

from app.models.schemas.post import Post
from app.utils.openapi import validate

bp = Blueprint("post", __name__, url_prefix="/api/post-service/v1/posts")


@bp.route("", methods=["POST"])
@validate()
def add_post(response: Post):
    return "hihi"
