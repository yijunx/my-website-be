from flask.testing import FlaskClient


def test_liveness(
    client: FlaskClient,
):
    resp = client.get(f"/internal/liveness")
    assert resp.status_code == 200
