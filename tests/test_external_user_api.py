from flask.testing import FlaskClient

SERVICE_NAME = "my-website-be"


def test_get_user_profile(client: FlaskClient, user_headers: dict, user_id: str):
    resp = client.get(
        f"/apis/{SERVICE_NAME}/v1/users/{user_id}/profile", headers=user_headers
    )
    assert resp.status_code == 200
