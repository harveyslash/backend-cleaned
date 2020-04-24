from flask import request
from flask_login import current_user
from sqlalchemy import and_, exc
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, requires_roles, \
    requires_validation
from extensions import db
from models import College, CollegeTest, Error, Order, OrderTest, Test, \
    TestAttempt, Section, Question
from .req_val import CollegeInputs

colleges_controller = JSONifiedNestableBlueprint("Colleges", __name__)


@colleges_controller.route('/colleges', methods=['GET'])
def get_colleges():
    """
    Returns list of Colleges
    :return: [colleges.todict()]
    """
    colleges = College.query \
        .options(load_only("college_name")) \
        .all()
    return colleges


@colleges_controller.route('/colleges/<path:college_id>', methods=['GET'])
def get_college(college_id):
    """
    Return details for a College
    :return: [college.todict()]
    """
    try:
        college = College.query \
            .filter(College.id == college_id) \
            .one()
        return college
    except NoResultFound:
        return Error("Invalid College ID", 400)()


@colleges_controller.route('/colleges', methods=['POST'])
@requires_validation(CollegeInputs)
@requires_roles('admin')
def create_college():
    """
    Allows admin to create Promo Code for User's discount
    :param college_name:
    :param college_logo:
    :return:
    """
    req = request.get_json()
    try:
        college = College(**req)
        db.session.add(college)
        db.session.commit()
        return ""
    except exc.IntegrityError:
        return Error('College already exists', 400)()


@colleges_controller.route('/colleges/<path:college_id>', methods=['PUT'])
@requires_roles('admin')
def update_promo_code(college_id):
    """
    Allows admin to edit College Details
    :param college_id:
    :param college_name:
    :param college_logo:
    :return:
    """
    req = request.get_json()
    try:
        college = College.query.filter(College.id == college_id).one()

        for key, value in req.items():
            setattr(college, key, value)

        db.session.commit()
        return ""
    except (NoResultFound, exc.IntegrityError):
        return Error('Invalid College ID/Parameters', 400)()


@colleges_controller.route('/colleges/profile', methods=['GET'])
def get_college_profile():
    if not current_user.is_authenticated:
        college_id = None
    else:
        college_id = current_user.college_id

    college_tests = (CollegeTest
        .query
        .join(CollegeTest.test)
        .options(contains_eager(CollegeTest.test))
        .options(load_only(CollegeTest.test_id, CollegeTest.is_free,
                           CollegeTest.is_active))
        .filter(
            CollegeTest.college_id == college_id)
    ).all()

    test_ids = [college_test.test_id for college_test in college_tests]

    current_user_id = current_user.id if not current_user.is_anonymous else None

    # this has been copied from Tests.py (list tests)

    tests = (Test.query
             .filter_by(**request.args)
             .filter(Test.id.in_(test_ids))
             .join(CollegeTest, and_(
            CollegeTest.test_id == Test.id,
            CollegeTest.college_id == current_user.college_id,
            CollegeTest.is_active == True,
    ))
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
        for order in test['orders']:
            test['status'] = order['status']
            if order['status'] == "paid":
                test['is_purchased'] = True

        # if len(test['orders']) > 0 :  # if a paid order exists
        #     test['is_purchased'] = True  # set is purchased to true

        for college_test in college_tests:
             if college_test.test_id == test['id'] and college_test.is_free:
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
