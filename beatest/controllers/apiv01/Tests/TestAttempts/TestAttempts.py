from datetime import datetime

from flask import Response
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only, eagerload, undefer
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, requires_roles
from Util import Pinger
from extensions import db
from models import Choice, Error, Question, QuestionAttempt, Section, \
    SectionAttempt, Test, TestAttempt, AuditLog

__author__ = "Harshvardhan Gupta"

test_attempt_controller = JSONifiedNestableBlueprint(
        "TestAttempt", __name__)


@test_attempt_controller.route('/tests/<test_id>/attempts/start', methods=[
    'Post'])
@login_required
def start_test(test_id):
    """
    Start a test.

    If an existing test_attempt that is not complete exists, it is returned.
    If not, if the user has access to the test, a new test attempt and section
    attempt(s) is created and returned.

    :param testID:
    :return: the id of the test attempt
    """

    try:
        attempt = (TestAttempt.query
                   # can be made inner join because section attempts should
                   # exist if question attempt exists

                   .join(TestAttempt.section_attempts)
                   .options(contains_eager(TestAttempt.section_attempts))
                   .filter(TestAttempt.test_id == test_id)
                   .filter(TestAttempt.user_id == current_user.id)

                   .one()
                   )

        if attempt.is_complete:
            return Error("Test is already completed", 403, "TAC001")()

        sorted_section_attempts = sorted(attempt.section_attempts,
                                         key=lambda x: x.id)

        current_section = (
            filter(lambda x: x.is_complete == False,
                   sorted_section_attempts)
        )

        # todo penalize the current_section by the value of
        # Pinger's time.

        current_section_id = list(current_section)[0].section_id

    except NoResultFound:  # didn't find existing attempt, create a new one

        if not Test.user_has_access(current_user, test_id):
            return Error("Purchase the Test", 400)()

        current_section_id = TestAttempt.setup_test_attempt(test_id,
                                                            current_user.id)

    test = (Test.query
            .filter(Test.id == test_id)
            .options(load_only(Test.allow_section_jumps))
            .one()
            )

    # finally, update the cookie
    string = Pinger.push_data_from_data(test_id,
                                        current_section_id,
                                        test.allow_section_jumps == True,
                                        datetime.timestamp(
                                                datetime.now()) + Pinger.PING_GRACE,
                                        0
                                        )

    resp = Response()
    resp.headers["ping"] = string

    AuditLog.log_start_test_event(user_id=current_user.id, test_id=test_id,
                                  current_section_id=current_section_id)

    return resp


@test_attempt_controller.route('/tests/<test_id>/attempts/finish', methods=[
    'Post'])
@login_required
def finish_test(test_id):
    """
    Finish a test for a user.
    This requires an active test attempt for the user with test id = test_id to
    exist.

    This endpoint will mark the is_complete column of the test_attempt to True.
    It will also calculate the score for the test attempt.

    :param test_id:
    """

    try:
        TestAttempt.calculate_score_for_test(current_user.id,
                                             test_id,
                                             should_persist=True)
    except NoResultFound:
        return Error("Not Found", 404)()


@test_attempt_controller.route('/tests/<test_id>/attempts',
                               methods=['Get'])
@login_required
def test(test_id):
    try:
        attempt = (TestAttempt.query
                   .join(TestAttempt.section_attempts)
                   .join(SectionAttempt.question_attempts)

                   .options(contains_eager(TestAttempt.section_attempts)
                            .load_only(SectionAttempt.section_id,
                                       SectionAttempt.is_complete,
                                       SectionAttempt.time_spent,
                                       SectionAttempt.score)
                            .contains_eager(SectionAttempt.question_attempts)

                            .load_only(QuestionAttempt.question_id,
                                       QuestionAttempt.choice_id,
                                       QuestionAttempt.tita_choice,
                                       QuestionAttempt.attempt_status,
                                       QuestionAttempt.question_id,
                                       QuestionAttempt.chosen_language_id,
                                       QuestionAttempt.time_spent,
                                       QuestionAttempt.score,

                                       # todo load this through an api if its too slow
                                       QuestionAttempt.long_answer
                                       ))

                   .filter(TestAttempt.test_id == test_id)
                   .filter(TestAttempt.user_id == current_user.id)
                   .one())


    except NoResultFound:
        return Error("Please start the test first", 403)()

    return attempt


@test_attempt_controller.route('/admin/tests/attempts/<testAttemptId>',
                               methods=["Delete"])
@requires_roles('admin')
@login_required
def delete_test_attempt(testAttemptId):
    test_attempt = (TestAttempt.query
                    .outerjoin(TestAttempt.section_attempts)
                    .outerjoin(SectionAttempt.question_attempts)
                    .filter(TestAttempt.id == testAttemptId)
                    .one())

    db.session.delete(test_attempt)

    db.session.commit()


@test_attempt_controller.route('/tests/<test_id>/attempts/performance',
                               methods=["Get"])
@login_required
def get_performance(test_id):
    """
    Get performance data of a particular test_id for the current user

    """

    try:

        test_attempt = (TestAttempt.query
                        .join(TestAttempt.section_attempts)
                        .join(SectionAttempt.section)
                        .join(SectionAttempt.question_attempts)
                        .join(QuestionAttempt.question)
                        .options(
                contains_eager(
                        TestAttempt.section_attempts)
                    .contains_eager(SectionAttempt.section))
                        .options(
                contains_eager(TestAttempt.section_attempts)
                    .undefer(SectionAttempt.total_question_count)
                    .contains_eager(SectionAttempt.question_attempts)
                    .load_only(QuestionAttempt.time_spent)
                    .contains_eager(QuestionAttempt.question)
                    .load_only(Question.lod, Question.type, Question.topic)
        )

                        .filter(TestAttempt.is_complete == True)
                        .filter(TestAttempt.user_id == current_user.id)
                        .filter(TestAttempt.test_id == test_id)
                        .one()
                        )

        output = test_attempt.todict()
        metrics = TestAttempt.get_percentile_for_score(
                test_attempt.score,
                test_id)

        return {**output, **metrics}

    except NoResultFound:
        return Error("Not Found", 404)()


@test_attempt_controller.route('/tests/<test_id>/attempts/focus',
                               methods=['Post'])
@login_required
def track_focus_change(test_id):
    try:

        test_attempt = (TestAttempt.query
                        .filter(TestAttempt.user_id == current_user.id)
                        .filter(TestAttempt.is_complete == False)
                        .filter(TestAttempt.test_id == test_id)
                        .one()
                        )

        test_attempt.focus_lost_count += 1
        db.session.commit()
        AuditLog.log_focus_change_event(current_user.id, test_id)


    except NoResultFound:
        return Error("Not Found", 404)()
    pass
