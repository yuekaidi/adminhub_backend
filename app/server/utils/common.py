import importlib
from typing import Any

import stringcase
from bson import ObjectId
from fastapi import FastAPI

from app.server.conf import settings


def without_keys(d, keys):
    """
    return a copy of dictionary without the keys specified
    invalid = {"keyA", "keyB"}
    without_keys(my_dict, invalid)
    :param d:
    :param keys:
    :return:
    """
    return {x: d[x] for x in d if x not in keys}


def with_keys(d, keys):
    """
    return a copy of dictionary without the keys specified
    invalid = {"keyA", "keyB"}
    only_keys(my_dict, invalid)
    :param d:
    :param keys:
    :return:
    """
    return {x: d[x] for x in d if x in keys}


def clean_dict_helper(d):
    if isinstance(d, ObjectId):
        return str(d)

    if isinstance(d, list):  # For those db functions which return list
        return [clean_dict_helper(x) for x in d]

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: clean_dict_helper(v)})

    return d


def form_query(fields: list[tuple]) -> dict:
    query = {}
    for key, value in fields:
        if value is not ...:
            query[key] = value
    return query


def to_camel(string: str) -> str:
    return stringcase.camelcase(string)


def resolve_dotted_path(path: str) -> Any:
    """
    Retrieves attribute (var, function, class, etc.) from module by dotted path
    .. code-block:: python
        from datetime.datetime import utcnow as default_utcnow
        utcnow = resolve_dotted_path('datetime.datetime.utcnow')
        assert utcnow == default_utcnow
    :param path: dotted path to the attribute in module
    :return: desired attribute or None
    """
    splitted = path.split(".")
    if len(splitted) <= 1:
        return importlib.import_module(path)
    module, attr = ".".join(splitted[:-1]), splitted[-1]
    module = importlib.import_module(module)
    return getattr(module, attr)


def get_current_app() -> FastAPI:
    """
    Retrieves FastAPI app instance from the path, specified in project's conf.
    :return: FastAPI app
    """
    # TODO: cache this
    app = resolve_dotted_path(settings.fastapi_app)
    return app