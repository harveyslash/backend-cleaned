from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, Float
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import deferred, relationship, validates

from Sugar import Dictifiable
from extensions import db


class CodingCase(Dictifiable, db.Model):
    __tablename__ = 'coding_case'

    id = Column(Integer, Sequence('coding_case_id_seq'), primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    input = deferred(Column(LONGTEXT))
    right_output = deferred(Column(LONGTEXT))
    viewable_with_question = Column(Boolean, default=False)
    viewable_with_solution = Column(Boolean, default=False)

    points_correct = Column(Float, default=0, nullable=False)
    points_wrong = Column(Float, default=0, nullable=False)

    question = relationship('Question', back_populates='coding_cases')

    @validates('input')
    def validate_input(self, key, input):
        if input is not None:
            return input.replace("\r\n", "\n").replace("\r", "\n")

    @validates('right_output')
    def validate_right_output(self, key, right_output):
        if right_output is not None:
            return right_output.replace("\r\n", "\n").replace("\r", "\n")
