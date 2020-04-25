from flask import Response
from json2html import json2html
from sqlalchemy.orm import contains_eager

from Sugar import JSONifiedNestableBlueprint, requires_roles
from models import (Order, PromoCode, User)

admin_misc_controller = JSONifiedNestableBlueprint("Admin MISC", __name__)


@admin_misc_controller.route('/misc/promo_metrics', methods=['GET'])
def get_admin_promo_metrics():
    """
    Get promocode->orders->users as a table.

    This takes in a complex json object and uses json2html to make it
    a readable table.

    :return: the json in table format as *HTML* format
    """

    query = (PromoCode.query
             .outerjoin(PromoCode.orders)
             .outerjoin(Order.user)
             .options(contains_eager(PromoCode.orders)
                      .load_only(Order.user_id, Order.status)
                      .contains_eager(Order.user).load_only(User.email)
                      )
             .all())

    result = [promo.todict() for promo in query]

    for promo in result:
        cancelled_count = 0
        paid_count = 0
        created_count = 0
        for order in promo['orders']:
            if order['status'] == 'cancelled':
                cancelled_count += 1
            if order['status'] == 'created':
                created_count += 1
            if order['status'] == 'paid':
                paid_count += 1
            del order['id']

        promo['created_count'] = created_count
        promo['paid_count'] = paid_count
        promo['cancelled_count'] = cancelled_count

    return Response(json2html.convert(json=result))
