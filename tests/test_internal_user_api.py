from flask.testing import FlaskClient

from app.models.schemas.user import Wink


def test_wink(
    client: FlaskClient,
    user_headers: dict,
):
    resp = client.post(f"/apis/internal_user/v1/wink", headers=user_headers)
    assert resp.status_code == 200
    p = Wink(**resp.get_json()["payload"])
    assert p.role == "reader"
