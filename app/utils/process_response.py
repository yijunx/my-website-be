from typing import Optional

from flask import make_response
from pydantic import BaseModel


class ResponseModel[T](BaseModel):
    payload: Optional[T] = None
    message: Optional[str] = None


def create_response(
    response: BaseModel = None,
    message: str = None,
    status_code: int = 200,
    headers: dict = None,
    cookies: dict = None,
    cookies_to_delete: list[str] = None,
):
    """
    this function can be used for
    set cookie,
    remove cookie,
    and set headers in the response
    so that browser may react accordingly
    """
    # if response is None:
    #     r = CustomResponse(message=message)
    # else:
    r = ResponseModel[type(response)](payload=response, message=message)
    resp = make_response(
        r.model_dump(),
        status_code,
    )
    resp.headers["charset"] = "utf-8"
    if True:  # TODO set it to dev or stg env check pls
        resp.headers["Access-Control-Allow-Origin"] = "localhost:3000"
    if headers:
        for k, v in headers.items():
            resp.headers[k] = v
    if cookies:
        for k, v in cookies.items():
            resp.set_cookie(key=k, value=v, httponly=True, secure=True)
    if cookies_to_delete:
        for key in cookies_to_delete:
            resp.delete_cookie(key=key)
    return resp


if __name__ == "__main__":
    from datetime import datetime, timezone

    class Item(BaseModel):
        name: str
        job: Optional[str] = None
        created_at: datetime

    item = Item(name="tom", created_at=datetime.now(timezone.utc))
    c = ResponseModel[type(item)](payload=item, message="nihao")
    item = None
    d = ResponseModel[type(item)]()
    # -> {'payload': {'name': 'tom', 'job': None, 'created_at': datetime.datetime(2024, 5, 8, 9, 48, 5, 124428, tzinfo=datetime.timezone.utc)}, 'message': 'nihao'}
    # -> {'payload': None, 'message': None}
    print(c.model_dump())
    print(d.model_dump())
