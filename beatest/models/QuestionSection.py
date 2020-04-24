from collections import Sequence

from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import deferred, relationship

from Sugar import Dictifiable
from extensions import db


class QuestionSection(Dictifiable, db.Model):
    __tablename__ = 'question_section'

    section_id = Column(Integer, ForeignKey('section.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), primary_key=True)
    order = Column(Integer, nullable=False, default=1)

    question = db.relationship('Question', backref='question_section')
    section = db.relationship('Section', backref='question_section')
