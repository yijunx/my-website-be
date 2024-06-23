from flask import Flask

from app.apis.external_user import bp as external_user_bp
from app.apis.internal_user import bp as internal_user_bp
from app.apis.internal_util import bp as internal_util_bp
from app.services.user import UserServiceInterface
from app.utils.service_registration import register_services_func


def create_app(user_service: UserServiceInterface = None):
    a = Flask(__name__)
    register_services_func(app=a, user_service=user_service)
    a.register_blueprint(internal_user_bp)
    a.register_blueprint(internal_util_bp)
    a.register_blueprint(external_user_bp)
    return a


# app = create_app()

if __name__ == "__main__":
    app = create_app()
    for rule in app.url_map.iter_rules():
        print(rule.endpoint)  # internal_user.get_latest_alive_session
        print(rule.rule)  # /api/internal_user/v1/sessions/<session_id>
        print(rule.methods)  # {'HEAD', 'GET', 'OPTIONS'}
