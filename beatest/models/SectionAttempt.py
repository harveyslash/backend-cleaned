from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, select, \
    func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property

from Sugar import Dictifiable
from extensions import db
from models import QuestionAttempt


class SectionAttempt(Dictifiable, db.Model):
    __tablename__ = 'section_attempt'

    id = Column(Integer, Sequence('section_attempt_id_seq'), primary_key=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    test_attempt_id = Column(Integer,
                             ForeignKey('test_attempt.id', ondelete="CASCADE"))
    time_spent = Column("time_left", Integer)
    # fixme , change column in  database from time_left to time_spent

    score = Column(Integer, nullable=True)

    is_complete = Column(Boolean)

    # count of correct questions in this section
    # will be calculated after test is finished
    correct_question_count = Column(Integer, nullable=True)

    # count of wrong questions in this section
    # will be calculated after test is finished
    incorrect_question_count = Column(Integer, nullable=True)

    section = relationship("Section", back_populates="section_attempts")
    test_attempt = relationship("TestAttempt",
                                back_populates="section_attempts")

    question_attempts = relationship('QuestionAttempt',
                                     back_populates='section_attempt',
                                     cascade="all, delete-orphan")

    # this is added to enable auto complete
    # look at __hybrid_props to see what this actually does
    total_question_count = None
