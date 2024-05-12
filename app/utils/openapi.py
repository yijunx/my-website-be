import inspect
from functools import wraps
from typing import Callable

from flask import Flask, request
from pydantic import ValidationError

from app.utils.config import configurations
from app.utils.process_response import ResponseModel, create_response

PARAM = "param"
JSON_BODY = "body"
RESPONSE = "response"


def openapi():
    """validate and openapi"""

    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            b_model = func.__annotations__.get(JSON_BODY)
            q_model = func.__annotations__.get(PARAM)
            r_model = func.__annotations__.get(RESPONSE)
            # we can do the same for the form..

            if b_model:
                try:
                    kwargs[JSON_BODY] = b_model(**request.get_json())
                except ValidationError as e:
                    return create_response(status_code=400, message=str(e))

            if q_model:
                try:
                    kwargs[PARAM] = q_model(**request.args)
                except ValidationError as e:
                    return create_response(status_code=400, message=str(e))
            if r_model:
                # here acutally we can validate the result of
                # func(*args, **kwargs)
                kwargs[RESPONSE] = r_model

            return func(*args, **kwargs)

        return wrapper

    return decorate


def get_summary_desc(func) -> tuple[str, str]:
    """
    get summary, description from `func.__doc__`

    Summary and description are split by '\n\n'. If only one is provided,
    it will be used as summary.
    """
    doc = inspect.getdoc(func)
    if not doc:
        return func.__name__.capitalize(), ""
    doc = doc.split("\n\n", 1)
    if len(doc) == 1:
        return doc[0], ""
    return doc


def get_schema(t) -> dict:
    return ResponseModel[t].model_json_schema(
        ref_template="#/components/schemas/{model}"
    )


def generate_spec(app: Flask):

    routes = {}
    nested_schemas = {}

    for rule in app.url_map.iter_rules():

        if rule.rule.startswith("/static"):
            continue
        func = app.view_functions[rule.endpoint]
        # get the models
        b_model = func.__annotations__.get(JSON_BODY)
        q_model = func.__annotations__.get(PARAM)
        r_model = func.__annotations__.get(RESPONSE)
        # try:
        #     r_model = func.__response # added by the validate..
        # except:
        #     r_model = None

        if b_model or q_model or r_model:
            pass
        else:
            continue

        if rule.rule not in routes:
            routes[rule.rule] = {}
        for method in rule.methods:
            if method in ["HEAD", "OPTIONS"]:
                continue

            # now we have the method and the url
            # method is method
            # url is rule.rule

            summary, desc = get_summary_desc(func)
            params = []
            # path, parameters = parse_url(str(rule))

            spec = {
                "summary": summary,
                "description": desc,
                "operationId": func.__name__ + "__" + method.lower(),
                "tags": ["AllEndpoints"],
            }

            if b_model:
                nested_schemas[b_model.__name__] = get_schema(b_model)
                spec["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": f"#/components/schemas/{b_model.__name__}"
                            }
                        }
                    }
                }
            if q_model:
                nested_schemas[q_model.__name__] = get_schema(q_model)
                params.append(
                    {
                        "name": q_model.__name__,
                        "in": "query",
                        "required": True,
                        "schema": {
                            "$ref": f"#/components/schemas/{q_model.__name__}",
                        },
                    }
                )

            spec["parameters"] = params
            spec["responses"] = {}

            if r_model:
                nested_schemas[r_model.__name__] = get_schema(r_model)
                spec["responses"]["20X"] = {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": f"#/components/schemas/{r_model.__name__}"
                            }
                        }
                    },
                }

            routes[rule.rule][method.lower()] = spec
    unpacked_schemas = {}
    for _, model in nested_schemas.items():
        if "$defs" in model:
            for key, value in model["$defs"].items():
                # print(f"Adding {value} to {key}")
                unpacked_schemas[key] = value

    components = {
        "schemas": unpacked_schemas,
        # "securitySchemes": {
        #     "bearerAuth": {
        #         "type": "http",
        #         "scheme": "bearer",
        #         "bearerFormat": "JWT",
        #     }
        # },
    }
    data = {
        "openapi": "3.0.2",
        "info": {
            "service_name": configurations.SERVICE_NAME,
            "service_version": configurations.SERVICE_VERSION,
        },
        "paths": {**routes},
        "components": components,
    }
    return data


if __name__ == "__main__":
    from app.main import create_app

    d = generate_spec(create_app())
    print(d)
