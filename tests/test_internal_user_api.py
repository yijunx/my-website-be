from flask.testing import FlaskClient

from app.models.schemas.user import LoginSession


def test_login(
    client: FlaskClient,
    headers_with_id_token: dict,
    user_id: str,
    login_session_id: str,
):
    r = client.post(f"/api/internal_user/v1/login", headers=headers_with_id_token)
    assert r.status_code == 200
    l = LoginSession(**r.get_json()["payload"])
    assert l.user_id == user_id
    assert l.id == login_session_id
