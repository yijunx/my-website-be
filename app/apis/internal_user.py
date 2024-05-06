from flask import Blueprint

bp = Blueprint("internal_user", __name__)


@bp.route("/login", methods=["POST"])
def login():

    # will require
    # from the id token we save or update the user
    # if user login via different social, login, how do we know it is same user?
    # well lets rely on email, i guess..

    # this returns
    # user as well its its session, and session expiration
    ...


@bp.route("/session", methods=["GET"])
def get_latest_alive_session():
    # email in the query parameter
    ...
