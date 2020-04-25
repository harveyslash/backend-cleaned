from flask_login import current_user
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from Sugar import JSONifiedNestableBlueprint
from models import Course, Order, OrderCourse

courses_controller = JSONifiedNestableBlueprint("Courses", __name__)


@courses_controller.route('/courses', methods=['Get'])
def get_courses():
    """
    List all courses in the system.
    If user has purchased some, the courses will have 'is_purchased' key
    to true, else it will be false.

    If user has access to those courses by being in a college, the same thing
    applies.

    It also passes the query parameters received from the client
    as is , to the db queries. Useful for filtering

    """
    current_user_id = current_user.id if not current_user.is_anonymous else None

    # left outer join on course -> orders -> ordercourse. if user has a
    # paid order  it will be accessible by course.order.
    courses = (Course.query
               .outerjoin(OrderCourse,
                          OrderCourse.course_id == Course.id)
               .outerjoin(Order, and_(Order.id == OrderCourse.order_id,
                                      Order.status == 'paid',
                                      Order.user_id == current_user_id))
               .options(contains_eager(Course.orders)
                        .load_only(Order.status))
               .filter(Course.is_active == 1)
               .all())

    courses = [course.todict() for course in courses]

    for course in courses:
        course['is_purchased'] = False  # set key, false by default
        if len(course['orders']) > 0:  # if a paid order exists
            course['is_purchased'] = True  # set is purchased to true
        del course['orders']

    return courses
