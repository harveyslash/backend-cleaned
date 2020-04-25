from Sugar import JSONifiedNestableBlueprint, requires_validation
from controllers.rex import CookieHelper
from controllers.rex.CookieHelper import requires_corporate_cookies
from controllers.rex.Users.req_val import LoginInputs

from flask import request, Response, jsonify, session
from models import User, Error
from extensions import bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import contains_eager, load_only

from flask import session
# from flask_login import
from flask import current_app

rex_user_controller = JSONifiedNestableBlueprint('RexUser', __name__)


@rex_user_controller.route('/user/get_user_cookie/<user_id>', methods=['Post'])
def get_user_cookie(user_id):
    # current_app.login

    session_copy = {**session}
    user = User.query.get(user_id)

    print(current_user.is_anonymous)
    return

    login_user(user)
    # print(session)
    # return

    for key, value in session.items():
        session[key] = session_copy[key]

    return current_user

    pass
