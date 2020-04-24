from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship, deferred

from Sugar import Dictifiable
from extensions import db


class Choice(Dictifiable, db.Model):
    __tablename__ = 'choice'

    id = Column(Integer, Sequence('choice_id_seq'), primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    html = deferred(Column(LONGTEXT))
    is_correct = Column(Boolean)

    question = relationship('Question', back_populates='choices')
