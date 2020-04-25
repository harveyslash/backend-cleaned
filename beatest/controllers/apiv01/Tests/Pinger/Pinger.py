from flask import Response
from flask_login import current_user
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.exc import NoResultFound

from extensions import db

from Sugar import JSONifiedNestableBlueprint
from Util import Pinger
from models import (Section, Test, SectionAttempt, TestAttempt, Error,
                    QuestionAttempt)
from datetime import datetime

PingController = JSONifiedNestableBlueprint("Ping Controller", __name__)


@PingController.route(
        "/tests/<testID>/sections/<int:sectionID>/questions/<int:questionID>/attempts/ping",
        methods=["Post"])
def ping(testID, sectionID, questionID):
    """
    Perform 1 ping.
    The time spent on each section will be reduced by the Pinger's duration
    value.
    (Read how the logic works for sectional jumps vs non sectional jumps in the
    comments below).

    If all the requests succeed, then the pinger gets a new cookie with an
    updated time.
    If not, this operation will not happen, making future requests impossible.

    :param testID:
    :param sectionID:
    :param questionID:
    :return:
    """

    try:
        # for tests with jumps allowed, the section_id field is ignored
        # instead, we use the value passed by the client.

        test_id, section_id, jumps_allowed, _, warn_count = Pinger.validate_ping_time()
    except ValueError:
        return Error("Ping Time Too High", 403, Pinger.PING_TIME_FAIL_CODE)()

    # get TestAttempt -> Test
    # & TestAttempt->SectionAttempts->QuestionAttempts
    # & TestAttempt->SectionAttempts->Sections

    try:
        test_attempt = (TestAttempt.query
                        .filter(TestAttempt.test_id == test_id)
                        .filter(TestAttempt.user_id == current_user.id)
                        .filter(TestAttempt.is_complete == False)

                        .join(TestAttempt.test)
                        .join(TestAttempt.section_attempts)
                        .join(SectionAttempt.question_attempts)
                        .join(SectionAttempt.section)
                        .options(contains_eager(TestAttempt.test))
                        .options(contains_eager(TestAttempt.section_attempts)
                                 .contains_eager(
                SectionAttempt.question_attempts)
                                 .load_only(QuestionAttempt.section_attempt_id,
                                            QuestionAttempt.time_spent)
                                 )
                        .options(contains_eager(TestAttempt.section_attempts)
                                 .contains_eager(SectionAttempt.section))
                        .one()
                        )
    except NoResultFound:
        return Error("Test already complete or invalid data", 403)()

    if jumps_allowed:
        # Section jumps are allowed.
        # in this case,calculate total time spent by summing up each
        # section attempt.
        # Then the time is compared with one of the sections under the test
        # (each section should have the same total_time)
        # if the time spent is > total_time , the test is automatically
        # marked complete

        section_times = map(lambda section_att: section_att.time_spent,
                            test_attempt.section_attempts)

        section_attempt = list(filter(lambda
                                          section_attempt: section_attempt.section_id == sectionID,
                                      test_attempt.section_attempts))[0]

        section_attempt.time_spent += Pinger.PING_DURATION

        total_time_spent = sum(section_times)

        total_time = (
            list(map(lambda section_att: section_att.section.total_time,
                     test_attempt.section_attempts))[0])

        if total_time_spent >= total_time:
            # fixme this method call does the entire complicated
            # join once more. may be avoided
            TestAttempt.calculate_score_for_test(current_user.id, test_id,
                                                 should_persist=True)

    else:
        # Section jumps are not allowed.
        # in this case,calculate total time spent on the section by
        # checking the section from the session
        # if the time spent is > total sectional time , the section is
        # automatically marked complete

        section_attempt = list(filter(lambda
                                          section_attempt: section_attempt.section_id == section_id,
                                      test_attempt.section_attempts))[0]

        sorted_section_attempts = sorted(test_attempt.section_attempts,
                                         key=lambda
                                             section_attempt: section_id)

        section_attempt.time_spent += Pinger.PING_DURATION

        if section_attempt.time_spent >= section_attempt.section.total_time:
            section_attempt.is_complete = True

            # if the last section was just completed
            # then calculate score and mark the test complete
            if section_attempt.section_id == sorted_section_attempts[
                -1].section_id:
                TestAttempt.calculate_score_for_test(current_user.id,
                                                     test_id,
                                                     True)

    # question attempt time is updated from the UI directly
    # this block will be deleted soon.

    # for section_attempt in test_attempt.section_attempts:
    #     for question_attempt in section_attempt.question_attempts:
    #         # print(question_attempt.question_id)
    #         # print(questionID)
    #         if question_attempt.question_id == questionID:
    #             # print("HERE")
    #             question_attempt.time_spent += Pinger.PING_DURATION

    db.session.commit()

    curr_time = datetime.timestamp(datetime.now())
    string = Pinger.push_data_from_data(test_id, section_id, jumps_allowed,
                                        curr_time, warn_count)
    resp = Response()
    resp.headers["ping"] = string
    return resp
