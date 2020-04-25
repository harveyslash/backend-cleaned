from flask import request
from flask_login import current_user, login_required
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Externals import Discourse
from Externals.Razorpay import Razorpay
from Sugar import JSONifiedNestableBlueprint, requires_validation
from extensions import db
from models import (Error, Order, OrderCourse, OrderTest, PromoCode,
                    Test)
from models.Order import OrderStatusTypes
from .req_val import OrderCreateInputs

__author__ = "Harshvardhan Gupta"
orders_controller = JSONifiedNestableBlueprint("Orders", __name__)


@orders_controller.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """
    List Orders for a User.

    Currently it lists test ids associated with the Order.
    If more items are added, all those will also need to be sent over.

    :return: [orders.todict()]
    """
    orders = (Order.query
              .filter_by(**request.args)
              .outerjoin(OrderTest)
              .outerjoin(Test)
              .options(contains_eager(Order.tests)
                       .load_only(Test.id, Test.name))
              .filter(Order.user_id == current_user.id)
              .all())
    return orders


@orders_controller.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """
    Order for the User based on Order ID. It will check if the Order belongs
    to the User.

    :param order_id:
    :return: order
    """
    try:
        order = (Order.query
                 .outerjoin(OrderTest)
                 .outerjoin(Test)
                 .options(contains_eager(Order.tests)
                          .load_only(Test.id))
                 .filter(Order.id == order_id)
                 .filter(Order.user_id == current_user.id)
                 .one())
        return order
    except NoResultFound:
        return Error('Invalid Order ID', 404)()


@orders_controller.route('/orders/<int:user_id>/<int:test_id>/status', methods=['GET'])
@login_required
def get_order_status(user_id, test_id):
    """
    Payment Status for a Order.

    :param user_id:
    :param test_id:
    :return: order_status
    """
    try:
        order = (Order.query
                 .outerjoin(OrderTest)
                 .outerjoin(Test)
                 .options(contains_eager(Order.tests)
                          .load_only(Test.id))
                 .filter(Test.id == test_id)
                 .filter(Order.user_id == user_id)
                 .one())

        return {'status': str(order.status).split(".")[1]}
    except NoResultFound:
        return {'status': 'new'}


@orders_controller.route('/orders', methods=['POST'])
@login_required
def create_order():
    """
    Creates Order row. Updates order with Razorpay Order ID. Inserts rows in
    Item tables with the Order ID
    :return: {'id': order.id, 'rp_order_id': razorpay_order_id}
    """
    req = request.get_json()
    test_ids = req['tests'] if req['tests'] is not None else []
    promo = req['promo_code']  # will be null if not present
    total_amount = 0

    promo_id = None
    razorpay_order_id = None  # set to null by default
    tests = Test.query \
        .filter(Test.id.in_(test_ids)) \
        .options(load_only('price')) \
        .all()

    for test in tests:
        total_amount += test.price

    total_amount = max(0, total_amount)

    if promo:
        try:
            promo_amt, promo_id = PromoCode.consume_promo_code(promo,
                                                               current_user.id)
            total_amount -= promo_amt
        except ValueError as e:
            return Error(str(e), 400)()

    order = Order(status=OrderStatusTypes.created,
                  amount=total_amount,
                  promo_code_id=promo_id,
                  user_id=current_user.id)

    db.session.add(order)
    db.session.flush()

    if total_amount > 0:
        razorpay_order_id = Razorpay.create_order(order.id, total_amount)
    else:
        order.status = OrderStatusTypes.paid  # mark free order as paid

    order.rp_order_id = razorpay_order_id

    # This adds rows to OrderTest which is important for User to get
    # access when Payment goes through
    for test in tests:
        test_id = test.id
        order_test = OrderTest(order_id=order.id, test_id=test_id)
        db.session.add(order_test)

    db.session.commit()

    return {'id': order.id, 'rp_order_id': razorpay_order_id}


@orders_controller.route('/orders/<path:rp_order_id>/status', methods=['PUT'])
@login_required
def update_order_payment_status(rp_order_id):
    """
    Updates the Payment status of Order after querying Razorpay. Will be
    mostly used for confirming payment after Checkout
    :param rp_order_id: razor pay order id
    :return: payment_status
    """
    try:
        order = (Order.query
                 .filter(Order.rp_order_id == rp_order_id)
                 .filter(Order.user_id == current_user.id)
                 # required for discourse
                 .one())

        status = Razorpay.get_order_status(order.rp_order_id)

        order.status = status
        db.session.commit()

        return {'payment_status': status}

    except NoResultFound:
        return Error('Invalid Order ID', 400)()


@orders_controller.route('/payments/capture', methods=['POST'])
@login_required
def capture_order():
    """
    Capture a payment in Razorpay
    """
    try:
        req = request.get_json()
        payment_id = req['payment_id']
        amount = req['amount']
        captured = Razorpay.capture_payment(payment_id, amount)
        return {'captured': captured}

    except NoResultFound:
        return Error('Invalid Order ID', 400)()


@orders_controller.route('/orders/<int:order_id>/cancel', methods=['PUT'])
@login_required
def cancel_order(order_id):
    """
    Mark the order as cancelled.It is only be possible to cancel
    if order status is not paid.
    """
    try:
        order = (Order
                 .query
                 .options(load_only(Order.id))
                 .filter(Order.user_id == current_user.id)
                 .filter(Order.id == order_id)
                 # order cannot be paid
                 .filter(Order.status != OrderStatusTypes.paid)
                 .one())

        order.status = OrderStatusTypes.cancelled
        db.session.commit()

        return ""
    except NoResultFound:
        return Error('Invalid Order ID', 400)()
