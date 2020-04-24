from flask_login import current_user, login_required
from sqlalchemy import and_
from Sugar import cachify

from Sugar import JSONifiedNestableBlueprint
from models import Error, Section, Test, TestAttempt
from .Questions import questions_controller
from .SectionAttempts import section_attmpt_ctrl

__author__ = "Harshvardhan Gupta"

sections_controller = JSONifiedNestableBlueprint(
        'Sections_controller', __name__)
sections_controller.register_blueprint(questions_controller)
sections_controller.register_blueprint(section_attmpt_ctrl)


@sections_controller.route('/tests/<test_id>/sections', methods=['Get'])
@cachify(1800)
@login_required
def get_sections(test_id):
    """
    Get list of sections for a particular test.
    This requires the test attempt for the user to exist for the test

    :param test_id:
    :return:
    """
    sections = (Section.query
                .join(Test)
                .join(TestAttempt, and_(
            TestAttempt.test_id == Test.id,
            TestAttempt.user_id == current_user.id,
            TestAttempt.test_id == test_id)).all())

    if not sections:
        return Error("Test Attempt Does not exist", 403)()

    return sections
