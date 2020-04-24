"""
A decorator to validate inputs.
If the input validation fails, this decorator will
return the errors back to the user. In this case, the request
will never reach the logic.

If the validation is successful, this decorator continues on to the
endpoint.

NOTE: this WILL REMOVE all keys that are not mentioned in the corresponding
        validator class.

This uses the schematics library behind the scenes to do the validation
"""

__author__ = "Harshvardhan Gupta"

from functools import wraps

from flask import request
from schematics.exceptions import BaseError

import json


def requires_validation(validator):
    from models import Error

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            try:
                if request.json:
                    handle_json(validator)
                elif request.form:
                    handle_form(validator)
                else:
                    return Error(message="Invalid request",
                                 http_code=400)()


            except BaseError as e:
                return Error(message="Invalid request", http_code=400,
                             additional=e.to_primitive())()

            return f(*args, **kwargs)

        return wrapped

    return wrapper


def handle_form(validator):
    body = request.form.get('body')

    try:
        json_req = json.loads(body)

    except:
        raise BaseError("")
    request.form = json_req

    form = validator(json_req)
    form.validate()
    cleaned = form.to_primitive()
    request.form = cleaned


def handle_json(validator):
    form = validator(request.json)
    form.validate()
    request.json.clear()
    cleaned = form.to_primitive()
    for key in cleaned.keys():
        request.json[key] = cleaned[key]
