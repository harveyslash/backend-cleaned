from flask import session, jsonify

from models import Error
from functools import wraps


def set_corporate_cookie(corporate_id):
    session["corporate_id"] = corporate_id


def get_corporate_id():
    return session['corporate_id']


def requires_corporate_cookies():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                corporate_id = session["corporate_id"]
                if corporate_id < 1:
                    raise Exception
            except:
                return Error("Invalid Cookies present", 403)()
            return f(*args, **kw)

        return wrapper

    return decorator
