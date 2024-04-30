from flask import Flask
from app.apis.internal_user import bp as internal_user_bp


app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(internal_user_bp, url_prefix="/apis/internal_user/v1")
    return app
