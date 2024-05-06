# -------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
# -------------------------------------------------------------------------------------------------------------
from typing import Optional

from flask import make_response
from pydantic import BaseModel


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
    resp = make_response(
        {"data": response.model_dump_json(), "message": message},
        status_code,
    )
    resp.headers["charset"] = "utf-8"
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

    data = Item(name="tom", created_at=datetime.now(timezone.utc))
    print(data.model_dump_json())
