"""
Adds Support for Browser Based caching.
This adds the required headers in the response.

Usage:
    from Sugar import Cachify   # this import is required

    @controller.route('/some/route/') # route definition as usual
    @cachify(timeout=500)  # timeout value in seconds (Default is 120 seconds)

"""
from functools import wraps
from flask import make_response
from flask import jsonify
from flask import Response

__author__ = "harshvardhan gupta"


def cachify(timeout=120):
    """
    A decorator to add cache control headers to cache a particular endpoint.

    :param timeout: the timeout value in seconds (default is 120 seconds)
    :return: a function that returns a decorator.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = f(*args, **kwargs)

            try:

                resp = jsonify(resp)

                if resp.status_code < 300:
                    resp.headers['cache-control'] = f"max-age={timeout}"
            except:
                pass

            return resp

        return decorated_function

    return decorator
