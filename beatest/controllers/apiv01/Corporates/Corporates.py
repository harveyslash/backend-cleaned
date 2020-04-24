from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint
from models import Corporate, Error

corporates_controller = JSONifiedNestableBlueprint("Corporates", __name__)


@corporates_controller.route('/corporates/<path:corporate_slug>',
                             methods=['GET'])
def get_corporate(corporate_slug):
    try:
        corporate = Corporate.query \
            .filter(Corporate.slug == corporate_slug) \
            .one()
        return corporate
    except NoResultFound:
        return Error("Invalid Corporate Slug", 400)()
