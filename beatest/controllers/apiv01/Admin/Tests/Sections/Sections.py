from flask import request
from sqlalchemy.orm.exc import NoResultFound

from Sugar import JSONifiedNestableBlueprint, requires_validation
from extensions import db
from models import Choice, Error, Question
from .req_val import QuestionInputs

__author__ = "Harshvardhan Gupta"
# All endpoints will have sectionID in them, so it is prepended
# to the nestable controller


admin_sections_controller = JSONifiedNestableBlueprint(
    "Admin Sections", __name__)


@admin_sections_controller.route('/<sectionId>/questions', methods=['GET'])
def get_admin_section_questions(sectionId):
    """
    List Questions of a Section for Admin based on the Section ID
    :param sectionId:
    :return: questions
    """
    try:
        questions = Question.query \
            .filter(Question.section_id == sectionId)\
            .all()

        return questions
    except NoResultFound:  # section id is incorrect
        return Error('Invalid Section ID', 400)()


@admin_sections_controller.route('/<sectionId>/questions', methods=['POST'])
@requires_validation(QuestionInputs)
def create_admin_section_question(sectionId):
    """
    Create Section Question
    :param sectionId:
    :return:
    """
    req = request.get_json()
    req['section_id'] = sectionId

    question = Question(**req)

    db.session.add(question)
    db.session.commit()

    return ""


@admin_sections_controller.route('/questions/<questionId>', methods=['GET'])
def get_admin_section_question(questionId):
    """
    Question Details based on Question ID
    :param questionId:
    :return: questions
    """
    try:
        question = Question.query \
            .filter(Question.id == questionId)\
            .one()

        return question
    except NoResultFound:  # section id is incorrect
        return Error('Invalid Question ID', 400)()


@admin_sections_controller.route('/questions/<questionId>', methods=['DELETE'])
def delete_admin_section_question(questionId):
    """
    Question Details based on Question ID
    :param questionId:
    :return:
    """
    try:
        Choice.query\
            .filter(Choice.question_id == questionId)\
            .delete(synchronize_session='fetch')

        Question.query \
            .filter(Question.id == questionId)\
            .delete(synchronize_session='fetch')

        return ""
    except NoResultFound:  # question id is incorrect
        return Error('Invalid Question ID', 400)()
