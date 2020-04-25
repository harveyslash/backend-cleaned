"""
Routes mapping for Admin api version 0.1. This allows for nestable
routing. Sub controllers under admin api v0.1. need to be
'registered' by importing them. The sub controllers need to
import the base blue-print from this file in order to be registered.
"""

__author__ = "Harshvardhan Gupta"

from datetime import datetime

from flask_login import current_user, login_required

from Sugar import JSONifiedNestableBlueprint
from extensions import db
from models import Error, Role, UserRoles
from .Misc import admin_misc_controller

admin_base_blueprint = JSONifiedNestableBlueprint('admin_api', __name__)

admin_base_blueprint.register_blueprint(admin_misc_controller)


# admin_base_blueprint.register_blueprint(admin_tests_controller)

@admin_base_blueprint.before_request
@login_required
def verify_admin():
    """
    Checks if the current user has an admin role.
    It also means that the user must be logged in.

    This function will be applied to all endpoints that use admin blueprint.
    :return:
    """

    query = UserRoles.query.join(UserRoles.role) \
        .filter(Role.name == 'admin') \
        .filter(UserRoles.user_id == current_user.id) \
        .exists()

    if not db.session.query(query).scalar():
        return Error("Unauthorized", 403)()


@admin_base_blueprint.route('', methods=['GET'])
def admin_echo_time():
    """
    Just a function to echo current time.
    May be useful for testing if servers are up.
    :return: current date
    """

    return datetime.now()
