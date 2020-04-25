from functools import wraps

from flask_login import current_user

from extensions import db


def requires_roles(*roles):
    """
    Role checker for custom roles. This function performs a lookup
    on the UserRoles table. An entry for the requested role must be present
    in UserRoles table.
    :param roles: a string with the requested role
    :return: if role doesnt exist, return with 403 forbidden,
            else continue with request
    """

    from models import Error
    from models.Role import Role
    from models.UserRoles import UserRoles
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            assert len(roles) == 1 and type(roles[0]) is str, \
                "first argument is not a string"

            if not current_user.is_authenticated:
                return Error("Not Logged in", 400)()

            query = UserRoles.query.join(UserRoles.role) \
                .filter(Role.name == roles[0]) \
                .filter(UserRoles.user_id == current_user.id) \
                .exists()

            if not db.session.query(query).scalar():
                return Error("Unauthorized", 403)()
            return f(*args, **kwargs)

        return wrapped

    return wrapper
