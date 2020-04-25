from flask import request
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, cachify
from models import Error, Order, OrderTest, Test, TestAttempt, Section, \
    Question
from .Sections import sections_controller
from .TestAttempts import test_attempt_controller

from .Pinger import PingController

tests_controller = JSONifiedNestableBlueprint("Tests", __name__)

tests_controller.register_blueprint(test_attempt_controller)

tests_controller.register_blueprint(sections_controller)

tests_controller.register_blueprint(PingController)


@tests_controller.route('/tests', methods=['Get'])
def get_tests():
    """
    List all tests in the system.
    If user has purchased some, the tests will have 'is_purchased' key
    to true, else it will be false.

    If user has access to those tests by being in a college, the same thing
    applies.

    It also passes the query parameters received from the client
    as is , to the db queries. Useful for filtering

    """
    current_user_id = current_user.id if not current_user.is_anonymous else None

    # left outer join on tests -> orders -> ordertest. if user has a
    # paid order  it will be accessible by test.order.
    # Only those tests that are not available for the user's college
    # will be fetched
    #
    # there is also a left outer join on tests -> testAttempts to get status
    # (is complete or not)
    #

    if 'type' not in request.args:
        return Error("", 404)()

    tests = (Test.query
             .filter_by(**request.args)
             .outerjoin(Test.sections)
             .outerjoin(Section.questions)
             .outerjoin(OrderTest,
                        OrderTest.test_id == Test.id)
             .outerjoin(Order, and_(Order.id == OrderTest.order_id,
                                    Order.user_id == current_user_id))
             .outerjoin(TestAttempt, and_(
            TestAttempt.test_id == Test.id,
            TestAttempt.is_complete == 1,
            TestAttempt.user_id == current_user_id
    ))
             .options(contains_eager(Test.sections)
                      .load_only(Section.id, Section.total_time)
                      .contains_eager(Section.questions)
                      .load_only(Question.id))
             .options(contains_eager(Test.test_attempts)
                      .load_only(TestAttempt.is_complete)
                      )
             .options(
            load_only(Test.id, Test.name, Test.character, Test.price,
                      Test.type, Test.logo, Test.allow_section_jumps))
             .options(contains_eager(Test.orders)
                      .load_only(Order.status))
             .filter(Test.is_active == 1)
             .all())

    fields = ['id',
        'name',
        'character',
        'allow_section_jumps',
        'price',
        'logo',
        'orders',
        'sections',
        {'sections': ['id', 'total_time', 'questions', {'questions': 'id'}]},
        'type',
        'test_attempts',
        {'orders':
            ['status']
        },
        {'test_attempts':
            ['is_complete']}
    ]
    tests = [test.todict(fields) for test in tests]

    # begin with paid tests #
    for test in tests:
        test['is_purchased'] = False  # set key, false by default
    #    if len(test['orders']) > 0:  # if a paid order exists
    #        test['is_purchased'] = True  # set is purchased to true
        for order in test['orders']:
            test['status'] = order['status']
            if order['status'] == "paid":
                test['is_purchased'] = True
        del test['orders']

        test['is_complete'] = False  # set key , false by default

        if len(test['test_attempts']):
            test['is_complete'] = True

        del test['test_attempts']

        question_count = 0
        section_count = 0

        total_time = 0
        for section in test["sections"]:
            section_count += 1
            total_time += section['total_time']

            for question in section["questions"]:
                question_count += 1

        test['section_count'] = section_count
        test['question_count'] = question_count
        test['total_time'] = total_time

        del test['sections']

    return tests


@tests_controller.route('/tests/<testID>', methods=['Get'])
# @login_required
# @cachify(60 * 60 * 12)
def get_test(testID):
    """
    Get Instruction html of a particular Test.
    This will return the html only if the user has access to a test.

    """

    # left outer join on tests -> orders -> ordertest. if user has a
    # paid order  it will be accessible by test.order.

    try:
        # if not Test.user_has_access(current_user, testID):
        #     raise NoResultFound

        test = (Test.query
                .options(
                load_only(Test.id, Test.name, Test.character, Test.price,
                          Test.instruction_html,
                          Test.type,
                          Test.allow_section_jumps))

                .filter(Test.is_active == 1)
                .filter(Test.id == testID)
                .one())


    except NoResultFound:
        return Error("You do not have access to this test", 403)()

    return test
