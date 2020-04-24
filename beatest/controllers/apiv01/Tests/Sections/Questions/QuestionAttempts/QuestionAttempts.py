"""
Question Attempts Module.

http://docs.beatest.in/api-v0.1/QuestionAttempts/

"""

from flask import request
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Externals import CaaS
from Sugar import JSONifiedNestableBlueprint, requires_validation
from Util import Pinger
from extensions import db
from models import (Error, QuestionAttempt, SectionAttempt, TestAttempt,
                    AuditLog)
from .req_val import RunCodeInputs, UpdateQuestionInputs, \
    UpdateQuestionTimeInputs

__author__ = "Harshvardhan Gupta"

qstn_attmpt_ctrl = JSONifiedNestableBlueprint("Question Attempt "
                                              "Controller", __name__)


@qstn_attmpt_ctrl.route('/tests/<testID>/sections/questions/<questionID>'
                        '/attempts/time_track')
@login_required
def track_time(testID, questionID):
    """
    TODO DELETE THIS API.

    Update the time by 5 seconds.

    This endpoint will fail if exactly one active test(with id=testID) for the
    current user is not present.

    :param testID:
    :param questionID:
    :return: 200 OK if update was successful, 403 error if exactly 1 test
            attempt was not found
    """

    try:

        # do a join from
        # TestAttempt -> SectionAttempts -> QuestionAttempt -> Question
        test_attempt = TestAttempt.query \
            .join(TestAttempt.section_attempts) \
            .join(SectionAttempt.question_attempts) \
            .join(QuestionAttempt.question) \
 \
            .options(contains_eager(TestAttempt.section_attempts)
                     .contains_eager(SectionAttempt.question_attempts)
                     .contains_eager(QuestionAttempt.question)) \
 \
            .filter(TestAttempt.test_id == testID) \
            .filter(TestAttempt.is_complete == False) \
            .filter(QuestionAttempt.question_id == questionID) \
            .filter(TestAttempt.user_id == current_user.id) \
            .one()

        test_attempt.section_attempts[0].question_attempts[0].time_spent += 5
        test_attempt.section_attempts[0].time_spent += 5

        db.session.commit()

        return ""
    except NoResultFound:
        return Error("Invalid details", 403)()


@qstn_attmpt_ctrl.route(
        '/tests/<testID>/sections/<sectionID>/questions/<questionID>/attempts',
        methods=['PUT'])
@login_required
@requires_validation(UpdateQuestionInputs)
def update_question(testID, sectionID, questionID):
    try:
        _, section_id, jumps_allowed, _, _ = Pinger.validate_ping_time()
        if not jumps_allowed:
            sectionID = section_id

        if 'chosen_language_id' in request.json:
            if not QuestionAttempt.can_use_coding_language(
                    request.json['chosen_language_id'],
                    questionID):
                return Error("Cant use this language", 403)()

        questionAttempt = (QuestionAttempt.query
                           .options(load_only(QuestionAttempt.question_id))
                           .filter(
                QuestionAttempt.question_id == questionID)
                           .join(SectionAttempt,
                                 and_(
                                         QuestionAttempt.section_attempt_id == SectionAttempt.id,
                                         SectionAttempt.is_complete == False,
                                         SectionAttempt.section_id == sectionID)
                                 )
                           .join(TestAttempt,
                                 and_(
                                         TestAttempt.id == SectionAttempt.test_attempt_id,
                                         TestAttempt.user_id == current_user.id,
                                         TestAttempt.test_id == testID,
                                         TestAttempt.is_complete == False)
                                 )
                           .one()
                           )

        AuditLog.log_question_attempt_update(user_id=current_user.id,
                                             test_id=testID,
                                             section_id=section_id,
                                             question_id=questionID,
                                             modified_key_vals=request.json)

    except ValueError:
        return Error("Ping Fail try again", 403, Pinger.PING_FAIL_TRY_AGAIN)()

    except NoResultFound:
        return Error("Data not found", 404, Pinger.PING_ALREADY_MOVED_ON)()

    [setattr(questionAttempt, key, value) for key, value in
        request.json.items()]

    db.session.commit()


@qstn_attmpt_ctrl.route(
        '/tests/<testID>/sections/<sectionID>/questions/<questionID>/attempts/time',
        methods=['PUT'])
@login_required
@requires_validation(UpdateQuestionTimeInputs)
def update_question_time(testID, sectionID, questionID):
    time = request.json['time']

    try:
        # _, section_id, jumps_allowed, _, _ = Pinger.validate_ping_time()
        # if not jumps_allowed:
        #     sectionID = section_id

        questionAttempt = (QuestionAttempt.query
                           .filter(
                QuestionAttempt.question_id == questionID)
                           .join(SectionAttempt,
                                 and_(
                                         QuestionAttempt.section_attempt_id == SectionAttempt.id,
                                         SectionAttempt.is_complete == False,
                                         SectionAttempt.section_id == sectionID)
                                 )
                           .join(TestAttempt,
                                 and_(
                                         TestAttempt.id == SectionAttempt.test_attempt_id,
                                         TestAttempt.user_id == current_user.id,
                                         TestAttempt.test_id == testID,
                                         TestAttempt.is_complete == False)
                                 )
                           .one()
                           )

        AuditLog.log_question_attempt_update(user_id=current_user.id,
                                             test_id=testID,
                                             section_id=sectionID,
                                             question_id=questionID,
                                             modified_key_vals=
                                             {'time': time}
                                             )


    except ValueError:
        return Error("Ping Fail try again", 403, Pinger.PING_FAIL_TRY_AGAIN)()

    except NoResultFound:
        return Error("Data not found", 404, Pinger.PING_ALREADY_MOVED_ON)()

    questionAttempt.time_spent += time

    db.session.commit()


@qstn_attmpt_ctrl.route('/coding/run', methods=['Post'])
@requires_validation(RunCodeInputs)
@login_required
def run_code():
    code = request.json['code']
    inputs = request.json['inputs']
    language = request.json['language_id']

    output = CaaS.get_outputs(code=code, inputs=inputs, language_id=language)

    return list(output)
