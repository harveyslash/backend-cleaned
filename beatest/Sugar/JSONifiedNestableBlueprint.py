"""
Nestable Blueprint to allow for
blueprints within blueprints. Useful for api namespacing.
Nesting appends to the url of the endpoints.

However, url_prefixes should be avoided because they make things
inflexible.

This module actually is used to add common behaviour for a group of similar
endpoints.


Additionally, all routes registered under this blueprint will also have
jsonify() called on them automatically.
"""
__author__ = "Harshvardhan Gupta"

from functools import wraps

from flask import Blueprint, Response, jsonify
from werkzeug.wrappers import Response as wResp


class JSONifiedNestableBlueprint(Blueprint):
    """
    A Flask.blueprint subclass that allows for blueprints within blueprints.
    Nested blueprints are defined exactly the same as Regular Blueprints.

    The difference is the added function register_blueprint().
    This mimics Flask.app's register_blueprints()

    This class will also call jsonify() on all routes that are registered
    under instances of this blueprint.

    Usage:

    In general, the child blueprint decides the full path.


    current_bluprint = NestedBlueprint("NAME",__name__)
    current_blueprint.route() # route definition like usual

    ...

    In the parent blueprint , import current_blueprint and then:

    parent_blueprint = NestedBlueprint("Parent_name",__name__)
    parent_blueprint.register_blueprint(current_blueprint)


    Notes:
        a parent blueprint's before_request methods will be executed for
        the child blueprint method too. This is an experimental feature.
        In the future , more methods may be added.

    """

    def __init__(self, *args, **kwargs):
        self.before_request_funcs = []
        super(JSONifiedNestableBlueprint, self).__init__(*args, **kwargs)

    def register_blueprint(self, blueprint, **options):

        def deferred(state):

            # register before_request functions of the parent blueprint
            # into the child blueprint
            # in the future more hooks like after_request can be added here
            for func in self.before_request_funcs[:]:
                blueprint.before_request(func)

            url_prefix = (state.url_prefix or u"") + (
                    options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(blueprint, url_prefix=url_prefix,
                                         **options)

        self.record(deferred)

    def before_request(self, f):
        self.before_request_funcs.append(f)
        return super().before_request(f)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        super().add_url_rule(rule,
                             endpoint,
                             jsonify_wrapper(view_func),
                             **options)


def jsonify_wrapper(func):
    """
    This takes in the response from a view, and jsonifies them automatically.

    it also handles the following:
        * handle None returns from views
                In this case, an empty body with 200 status will be sent
        * calls jsonify on data automatically
    :param func: the route function
    :return:  a function that when called, will call func and then jsonify the
                result
    """

    @wraps(func)
    def wrapper(**args):
        result = func(**args)
        # user intentionally wants to modify http code and/or headers
        if type(result) is tuple:

            if len(result) < 2:
                raise ValueError("Tuple returned in response, but has only 1 "
                                 "element. Maybe you have a stray comma?")
            data = result[0]
            status = result[1]
            headers = result[2] if len(result) == 3 else None
        # Explicit Response was sent, return to client without modifying
        elif type(result) is Response:
            return result
        elif type(result) is wResp:
            return result
        # valid data was returned , this will be jsonified automatically
        # and 200 response code will be set
        else:
            data = result
            status = 200
            headers = None

        # None or nothing was returned
        # this means empty body with 200 response should be sent
        if data is None:
            return jsonify()

        return jsonify(data), status, headers

    return wrapper
