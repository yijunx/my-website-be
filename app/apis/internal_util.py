from flask import Blueprint

bp = Blueprint("internal_util", __name__)


@bp.route("/internal/liveness", methods=["GET"])
def liveness():
    # check if the db is responsive here
    return {"hello": "i am alive"}
