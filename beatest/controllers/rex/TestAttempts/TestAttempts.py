from flask import request
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, requires_validation
from controllers.rex import CookieHelper
from controllers.rex.CookieHelper import requires_corporate_cookies
from controllers.rex.TestAttempts.req_val import ApplicationStatusTypes, \
    UpdateApplicants, UpdateScore
from extensions import db
from models import Corporate, CorporateApplicants, Error, QuestionAttempt, \
    SectionAttempt, TestAttempt, TestAttemptReport, SixteenPReport

rex_testattempts_controller = JSONifiedNestableBlueprint('RexTestAttempt',
                                                         __name__)


@rex_testattempts_controller.route('/test/<test_id>/attempts/<date>',
                                   methods=['Get'])
@requires_corporate_cookies()
def get_overview(test_id, date):
    if not Corporate.can_access_test(CookieHelper.get_corporate_id(),
                                     test_id):
        return Error("No access", 403)()

    return (Corporate.get_test_performance(CookieHelper.get_corporate_id(),
                                           test_id, date))


@rex_testattempts_controller.route(
        '/test/<test_id>/attempts/<date>/qualitative',
        methods=['Get'])
@requires_corporate_cookies()
def get_qualitative_analysis(test_id, date):
    if not Corporate.can_access_test(CookieHelper.get_corporate_id(),
                                     test_id):
        return Error("No access", 403)()

    return (Corporate.get_qualitative_analysis(CookieHelper.get_corporate_id(),
                                               test_id, date))


@rex_testattempts_controller.route(
        '/test/<test_id>/attempts/<date>/personality',
        methods=['Get'])
@requires_corporate_cookies()
def get_personality_analysis(test_id, date):
    if not Corporate.can_access_test(CookieHelper.get_corporate_id(),
                                     test_id):
        return Error("No access", 403)()

    return (Corporate.get_personality_analysis(CookieHelper.get_corporate_id(),
                                               test_id, date))

@rex_testattempts_controller.route(
        '/test/<test_id>/attempts/<date>/tabchange',
        methods=['Get'])
@requires_corporate_cookies()
def get_tab_change(test_id, date):
    if not Corporate.can_access_test(CookieHelper.get_corporate_id(),
                                     test_id):
        return Error("No access", 403)()

    return (Corporate.get_tab_change(CookieHelper.get_corporate_id(),
                                               test_id, date))


@rex_testattempts_controller.route('/applications',
                                   methods=['Put'])
@requires_corporate_cookies()
@requires_validation(UpdateApplicants)
def bulk_update_user_status():
    req = request.json
    user_ids = req['user_ids']
    new_status = req['status']

    applications = (CorporateApplicants.query
                    .filter(CorporateApplicants.user_id.in_(user_ids))
                    .filter(CorporateApplicants.corporate_id
                            == CookieHelper.get_corporate_id()
                            )
                    .all())

    for application in applications:
        application.type = ApplicationStatusTypes[new_status]

    db.session.commit()

    return applications


@rex_testattempts_controller.route('/test/<test_id>/dates', methods=['Get'])
@requires_corporate_cookies()
def get_test_dates(test_id):
    from sqlalchemy import func
    if not Corporate.can_access_test(CookieHelper.get_corporate_id(),
                                     test_id):
        return Error("No access", 403)()

    test_attempts = (
        TestAttempt.query
            .options(load_only(TestAttempt.date))
            .filter(TestAttempt.test_id == test_id)
            .filter(TestAttempt.is_complete == True)
            .filter(

                TestAttempt.user_id.in_(
                        db.session.query(
                                CorporateApplicants.user_id)
                            .filter(
                                CorporateApplicants.corporate_id == CookieHelper.get_corporate_id())
                )

        )

            .group_by(
                func.YEAR(func.CONVERT_TZ(TestAttempt.date,
                                          "+00:00",
                                          "-05:30")),
                func.MONTH(func.CONVERT_TZ(TestAttempt.date,
                                           "+00:00",
                                           "-05:30")),

                func.DAY(func.CONVERT_TZ(TestAttempt.date,
                                         "+00:00",
                                         "-05:30"))

        )

            .all())

    # print(test_attempts

    return test_attempts


@rex_testattempts_controller.route(
        '/test/attempts/<test_attempt_id>/sections/<section_attmpt_id>'
        '/questions/<question_id>',
        methods=['Get'])
@requires_corporate_cookies()
def update_question_attempt(test_attempt_id, section_attmpt_id,
                            question_id):
    test_attempt = (
        TestAttempt.query
            .filter(TestAttempt.id == test_attempt_id)
            .join(TestAttempt,
                  and_(CorporateApplicants.user_id == TestAttempt.user_id,
                       CorporateApplicants.corporate_id == CookieHelper.get_corporate_id()
                       )
                  )
            .join(SectionAttempt,
                  and_(SectionAttempt.test_attempt_id == TestAttempt.id,
                       SectionAttempt.id == section_attmpt_id))
            .join(QuestionAttempt,
                  and_(QuestionAttempt.section_attempt_id == SectionAttempt.id,
                       QuestionAttempt.question_id == question_id))
            .options(contains_eager(TestAttempt.section_attempts)
                     .contains_eager(SectionAttempt.question_attempts))
            .one()
    )


@rex_testattempts_controller.route(
        '/test/attempts/<test_attempt_id>/sections/<section_attmpt_id>'
        '/questions/<question_id>/score',
        methods=['Put'])
@requires_corporate_cookies()
@requires_validation(UpdateScore)
def update_question_attempt_score(test_attempt_id, section_attmpt_id,
                                  question_id):
    req = request.json

    test_attempt = (
        TestAttempt.query
            .filter(TestAttempt.id == test_attempt_id)
            .join(CorporateApplicants,
                  and_(CorporateApplicants.user_id == TestAttempt.user_id,
                       CorporateApplicants.corporate_id == CookieHelper.get_corporate_id()
                       )
                  )
            .join(SectionAttempt,
                  and_(SectionAttempt.test_attempt_id == TestAttempt.id,
                       SectionAttempt.id == section_attmpt_id))
            .join(QuestionAttempt,
                  and_(QuestionAttempt.section_attempt_id == SectionAttempt.id,
                       QuestionAttempt.question_id == question_id))
            .options(contains_eager(TestAttempt.section_attempts)
                     .contains_eager(SectionAttempt.question_attempts))
            .one()
    )

    score_diff = (
            req['score'] - test_attempt.section_attempts[0].question_attempts[
        0].score)

    test_attempt.section_attempts[0].score += score_diff
    test_attempt.section_attempts[0].question_attempts[0].score += score_diff
    test_attempt.score += score_diff

    db.session.commit()


@rex_testattempts_controller.route(
        '/tests/<test_id>/user/<user_id>', methods=['Get'])
@requires_corporate_cookies()
def get_test_attempt_report(test_id, user_id):
    if (not Corporate.can_access_test(CookieHelper.get_corporate_id(), test_id)
            or not Corporate.can_access_user(CookieHelper.get_corporate_id(),
                                             user_id)
    ):
        return Error("No access", 403)()

    report = (TestAttemptReport
              .query
              .join(TestAttempt,
                    and_(TestAttemptReport.test_attempt_id == TestAttempt.id,
                         TestAttempt.test_id == test_id,
                         TestAttempt.user_id == user_id))
              .one()
              )
    test_attempt = (TestAttempt.query
                    .filter(TestAttempt.test_id == test_id)
                    .filter(TestAttempt.user_id == user_id)
                    .one())

    report = report.todict()
    report['tab_change_count'] = test_attempt.focus_lost_count

    del report['test_attempt_id']
    del report['domain_based_ability']
    del report['paragraph_writing_ability']

    return report


@rex_testattempts_controller.route(
        '/tests/<test_id>/user/<user_id>/psych', methods=['Get'])
@requires_corporate_cookies()
def get_test_attempt_psych_report(test_id, user_id):
    if (not Corporate.can_access_test(CookieHelper.get_corporate_id(), test_id)
            or not Corporate.can_access_user(CookieHelper.get_corporate_id(),
                                             user_id)
    ):
        return Error("No access", 403)()

    try:

        report = (SixteenPReport
                  .query
                  .join(TestAttempt,
                        and_(SixteenPReport.test_attempt_id == TestAttempt.id,
                             TestAttempt.test_id == test_id,
                             TestAttempt.user_id == user_id))
                  .one()
                  )

    except NoResultFound:
        return Error("Not Found", 404)()

    report = report.todict()

    return report
