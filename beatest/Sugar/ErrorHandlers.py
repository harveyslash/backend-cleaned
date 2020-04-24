"""
Error Handling for flask.
This overrides the default html 404 , and instead
returns a json response 404.

It also overrides the default 500 html page.
"""

__author__ = "Harshvardhan Gupta"


def setup_error_handlers(app):
    """
    Set up error handlers.
    Other errors are called using jsonify() automatically,
    So no need to handle them.

    The errors below are raised by Flask , and we have to handle them
    manually.
    """
    from models import Error

    @app.errorhandler(404)
    def page_not_found(e):
        return Error("Page not found", 404, additional=str(e))()

    @app.errorhandler(500)
    def unknown_error(_):
        return Error(
                "Something went wrong. Our developer gnomes will be punished",
                500,
        )()

    @app.errorhandler(405)
    def method_not_allowed(e):
        return Error(
                "Method Not Allowed", 405,
                additional=str(e) if str(e) != "" else "")()

    @app.errorhandler(429)
    def too_many_requests(e):
        return Error(
                "Too many Requests", 429,
                additional=e.description)()
