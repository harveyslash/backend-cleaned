import csv

from sqlalchemy.orm import contains_eager, load_only
from tqdm import tqdm

from extensions import bcrypt, db
from models import TestAttempt, User, Section, Question, QuestionSection


def migrate_sections_to_many_to_many_command():
    questions = Question.query.options(load_only(Question.section_id)).filter(
            Question.section_id != None)

    for question in questions:
        print(question.section_id)
        print(question.id)

        question_section = QuestionSection(section_id=question.section_id,
                                           question_id=question.id)
        question_section.section_id = question.section_id
        question_section.question_id = question.id

        db.session.add(question_section)

    db.session.commit()
