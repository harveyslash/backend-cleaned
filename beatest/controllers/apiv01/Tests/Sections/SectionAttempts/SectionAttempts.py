from datetime import datetime

from flask import Response
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound
from extensions import db

from Sugar import JSONifiedNestableBlueprint
from Util import Pinger

from models import (Choice, Error, Question, Section, Test, TestAttempt,
                    SectionAttempt)

__author__ = "Harshvardhan Gupta"

section_attmpt_ctrl = JSONifiedNestableBlueprint(
        'section_attempt_controller', __name__)


@section_attmpt_ctrl.route(
        '/tests/<testID>/sections/<sectionID>/attempts/finish',
        methods=["Post"])
@login_required
def finish_section(testID, sectionID):
    try:
        test_id, section_id, jumps_allowed, _, _ = Pinger.split_pinger_string()
    except:
        return Error("No Pinger", 403)()

    try:

        test_attempt = (TestAttempt.query
                        .filter(TestAttempt.test_id == test_id)
                        .filter(TestAttempt.user_id == current_user.id)
                        .filter(TestAttempt.is_complete == False)
                        .join(TestAttempt.section_attempts)
                        .one()
                        )

    except NoResultFound:
        return Error("Data not found", 404)()
        pass

    sorted_section_attempts = sorted(test_attempt.section_attempts,
                                     key=lambda
                                         section_attempt: section_attempt.section_id)

    current_section_attempt = list(filter(
            lambda section_attempt: section_attempt.section_id == int(
                    section_id),
            sorted_section_attempts))[0]

    section_ids = [section.section_id for section in sorted_section_attempts]

    current_section_idx = section_ids.index(int(section_id))

    should_update = False

    # if there is an actual next section,
    # get its id , and update pinger
    if current_section_idx + 1 < len(section_ids):
        next_section_idx = section_ids[current_section_idx + 1]

        should_update = True

    current_section_attempt.is_complete = True
    db.session.commit()

    if should_update:
        string = Pinger.push_data_from_data(test_id, next_section_idx,
                                            jumps_allowed,
                                            datetime.timestamp(
                                                    datetime.now()) + Pinger.PING_GRACE,
                                            0)
        resp = Response()
        resp.headers["ping"] = string

        return resp
