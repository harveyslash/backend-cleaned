from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, cachify
from extensions import cache
from models import Choice, CodingCase, CodingLanguage, Error, Question, \
    TestAttempt
from .QuestionAttempts import qstn_attmpt_ctrl

__author__ = "Harshvardhan Gupta"

questions_controller = JSONifiedNestableBlueprint(
        'Questions_controller', __name__)

questions_controller.register_blueprint(qstn_attmpt_ctrl)


@cache.cached(timeout=6000)
def fetch_question(question_id):
    question = (Question.query
                .outerjoin(Question.choices)
                .outerjoin(CodingCase,
                           and_(Question.id == CodingCase.question_id,
                                CodingCase.viewable_with_question == True))
                .outerjoin(Question.allowed_languages)
                .options(
            load_only(Question.html, Question.rc_passage,
                      Question.coding_cases,
                      Question.type))
                .options(contains_eager(Question.choices)
                         .load_only(Choice.html))
                .options(
            contains_eager(Question.coding_cases)
                .load_only(CodingCase.input, CodingCase.right_output))
                .options(contains_eager(Question.allowed_languages)
                         .load_only(CodingLanguage.id, CodingLanguage.name)
                         )
                .filter(Question.id == question_id)
                .one())

    return question


@cache.cached(timeout=6000)
def fetch_solutions(question_id):
    question = (Question.query
                .outerjoin(Choice,
                           and_(Choice.question_id == Question.id,
                                Choice.is_correct == True))
                .outerjoin(CodingCase,
                           and_(Question.id == CodingCase.question_id,
                                CodingCase.viewable_with_solution == True))
                .options(contains_eager(Question.choices)
                         .load_only(Choice.is_correct))
                .options(
            load_only(Question.logic,
                      Question.lod,
                      Question.tita_answer,
                      Question.points_correct,
                      Question.points_wrong

                      ))
                .options(contains_eager(Question.coding_cases)
                         .load_only(CodingCase.input,
                                    CodingCase.right_output))
                .filter(Question.id == question_id).one())
    return question


@questions_controller.route(
        '/tests/<testID>/sections/<sectionID>/questions/<questionID>')
@login_required
@cachify(60 * 60 * 12)
def get_question_details(testID, sectionID, questionID):
    """
    Get question details for a questionID.
    This requires the test attempt for that user and the test to exist (along
    with section attempts)

    If the question has choices, they will be returned too


    FIXME there is a security vulnerability
    for non jumpable exams, the user may get unauthorized
    access to future sections' question details (that he will be allowed to
    attempt in the future)

    :param testID:
    :param sectionID:
    :param questionID:
    :return:
    """
    try:

        if not Question.does_user_have_access(testID, sectionID, questionID,
                                              current_user.id):
            raise NoResultFound

        question = fetch_question(questionID)


    except NoResultFound:
        return Error("Unable to find data", 403)()

    return question


@questions_controller.route(
        '/tests/<testID>/sections/<sectionID>/questions/<questionID>/solutions')
@login_required
@cachify(60 * 60 * 12)
def get_question_solutions(testID, sectionID, questionID):
    """
    Get question solutions details for a questionID.
    This requires the test attempt for that user and the test to exist (along
    with section attempts)

    If the question has choices, they will be returned too

    :param testID:
    :param sectionID:
    :param questionID:
    :return:
    """
    try:

        if not TestAttempt.can_user_view_solutions(current_user.id, testID):
            raise NoResultFound

        question = fetch_solutions(questionID)


    except NoResultFound:
        return Error("Unable to find data", 403)()

    return question
