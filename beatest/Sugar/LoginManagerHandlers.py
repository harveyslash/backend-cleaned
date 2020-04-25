"""
Setup functions for login manager.
It specifies how to find the user, given an id.
It also overrides the default behaviour of redirecting to login page.
Instead, it returns error code 401.
"""
__author__ = "Harshvardhan Gupta"
from sqlalchemy.orm.session import make_transient_to_detached
from extensions import db
from flask import session


def setup_login_manager(login_manager):
    from models import Error, User  # done to prevent cyclic dependency

    # @login_manager.user_loader
    # def load_user(user_id):
    #     print("this ")
    #     u = User(id=int(user_id))
    #     make_transient_to_detached(u)
    #     db.session.add(u)
    #     return u

    @login_manager.unauthorized_handler
    def unauthorized():
        return Error("You are not Logged in", 401)()

    @login_manager.request_loader
    def load_user_from_request(request):
        if 'user_id' not in session:
            return None

        if 'corporate_id' not in session:
            u = User(id=int(session['user_id']))
            make_transient_to_detached(u)
            db.session.add(u)
            return u

        if 'corporate_as_user' in request.headers:
            from models import Corporate
            if Corporate.can_access_user(session['corporate_id'],
                                         request.headers.get(
                                                 'corporate_as_user')):
                u = User(id=int(request.headers.get('corporate_as_user')))
                make_transient_to_detached(u)
                db.session.add(u)
                return u

        u = User(id=int(session['user_id']))
        make_transient_to_detached(u)
        db.session.add(u)
        return u
