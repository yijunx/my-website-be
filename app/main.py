from flask import Flask


from app.apis.internal_user import bp as internal_user_bp
from app.services.user import UserServiceInterface
from app.utils.service_registration import register_services_func


def create_app(user_service: UserServiceInterface = None):
    a = Flask(__name__)
    register_services_func(app=a, user_service=user_service)
    a.register_blueprint(internal_user_bp, url_prefix="/api/internal_user/v1")
    return a


app = create_app()
