from flask import request
from flask_login import current_user, login_required
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, requires_roles, \
    requires_validation
from extensions import db
from models import Error, PromoCode
from .req_val import PromoCodeInputs

promo_codes_controller = JSONifiedNestableBlueprint("PromoCodes",
                                                    __name__)


@promo_codes_controller.route('/promo_codes/', methods=['GET'])
@requires_roles('admin')
def get_promo_codes():
    """
    Returns all available Promo Codes in database
    :return: [promo.todict()]
    """
    try:
        promo_codes = PromoCode.query.all()
        return promo_codes
    except NoResultFound:
        return Error('Invalid Promo Code', 400)()


@promo_codes_controller.route('/promo_codes/<code>', methods=['GET'])
@requires_roles('admin')
def get_promo_code(code):
    """
    Fetch details based on Promo Code
    :param code:
    :return: promo.todict()
    """
    try:
        promo_code = PromoCode.query.filter(PromoCode.promo_code == code).one()
        return promo_code
    except NoResultFound:
        return Error('Invalid Promo Code', 400)()


@promo_codes_controller.route('/promo_codes', methods=['POST'])
@requires_validation(PromoCodeInputs)
@requires_roles('admin')
def create_promo_code():
    """
    Allows admin to create Promo Code for User's discount
    :param promo_code:
    :param promo_value:
    :param promo_max_usage:
    :param promo_valid:
    :param promo_multiple_use:
    :return:
    """
    req = request.get_json()
    try:
        promo_code = PromoCode(**req)
        db.session.add(promo_code)
        db.session.commit()
        return ""
    except exc.IntegrityError:
        return Error('Promo Code already exists', 400)()


@promo_codes_controller.route('/promo_codes/<promo_id>', methods=['PUT'])
@requires_roles('admin')
def update_promo_code(promo_id):
    """
    Allows admin to edit Promo Code. Below parameters are optional. Only
    provide the values that needs to updated.
    :param promo_code:
    :param promo_value:
    :param promo_max_usage:
    :param promo_valid:
    :param promo_multiple_use:
    :return:
    """
    req = request.get_json()
    try:
        promo_code = PromoCode.query.filter(PromoCode.id == promo_id).one()

        for key, value in req.items():
            setattr(promo_code, key, value)

        db.session.commit()
        return ""
    except NoResultFound:
        return Error('Invalid Promo Code', 400)()


@promo_codes_controller.route('/promo_codes/<code>/validate', methods=['POST'])
@login_required
def validate_promo_code(code):
    """
    Validates the promo code.
    For documentation on the conditions of how a user may consume a promo,
    visit Promocode.consume_promo_code

    :param code:
    :return:
    """
    try:
        promo_value, _ = PromoCode.consume_promo_code(code,
                                                      current_user.id,
                                                      should_flush=False)
        return {"promo_value": promo_value}
    except ValueError:
        return Error("Invalid Promo Code", 400)()
