from functools import wraps
from typing import Any, Callable, Iterable, List, Optional, Tuple, Type, Union

from flask import Flask, current_app, jsonify, make_response, request
from pydantic import BaseModel, ValidationError, TypeAdapter, RootModel

from app.utils.process_response import create_response, ResponseModel
import inspect
from app.utils.config import configurations


def validate():
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            b_model = func.__annotations__.get("body")
            q_model = func.__annotations__.get("query")

            if b_model:
                try:
                    kwargs["body"] = b_model(**request.get_json())
                except ValidationError as e:
                    return create_response(
                        status_code=400, message=str(e)
                    )
            
            if q_model:
                try:
                    kwargs["query"] = q_model(**request.args)
                except ValidationError as e:
                    return create_response(
                        status_code=400, message=str(e)
                    )

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
    return ResponseModel[t].model_json_schema(ref_template="#/components/schemas/{model}")


def generate_spec(app: Flask):

    routes = {}
    nested_schemas = {}

    for rule in app.url_map.iter_rules():

        if rule.rule.startswith("/static"):
            continue
        func = app.view_functions[rule.endpoint]
        # get the models
        b_model = func.__annotations__.get("body")
        q_model = func.__annotations__.get("query")
        r_model = func.__annotations__.get("response")
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
                "tags": ["All Endpoints"],
            }

            if b_model:
                nested_schemas[b_model.__name__] = get_schema(b_model)
                spec["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{b_model.__name__}"}
                        }
                    }
                }
            if q_model:
                nested_schemas[q_model.__name__] = get_schema(q_model)
                params.append({
                    "name": q_model.__name__,
                    "in": "query",
                    "required": True,
                    "schema": {
                        "$ref": f"#/components/schemas/{q_model.__name__}",
                    },
                })

            spec["parameters"] = params
            spec["responses"] = {}

            if r_model:
                nested_schemas[r_model.__name__] = get_schema(r_model)
                spec["responses"]["200"] = {
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
    real_schemas = {}
    for _, model in nested_schemas.items():
        if "$defs" in model:
            for key, value in model["$defs"].items():
                # print(f"Adding {value} to {key}")
                real_schemas[key] = value
            del model["$defs"]

    components = {
        "schemas": real_schemas,
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
        "info": {"service_name": configurations.SERVICE_NAME, "service_version": configurations.SERVICE_VERSION},
        "tags": [{"name": "All Endpoints"}],
        "paths": {**routes},
        "components": components,
    }
    return data

if __name__ == "__main__":
    from app.main import create_app
    d = generate_spec(create_app())
    print(d)




            

