import enum

from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db
from sqlalchemy.orm import deferred
from sqlalchemy.orm import contains_eager, load_only
from sqlalchemy import and_, or_


class QuestionTypesEnum(enum.Enum):
    tita = "TITA"
    rc = "RC"
    mcq = "MCQ"
    coding = "CODING"
    subjective = "SUBJECTIVE"


class Question(Dictifiable, db.Model):
    __tablename__ = 'question'

    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    html = deferred(Column(LONGTEXT))
    points_correct = Column(Float, default=0, nullable=False)
    points_wrong = Column(Float, default=0, nullable=False)
    type = Column(String(50))
    tita_answer = Column(LONGTEXT)
    rc_passage = deferred(Column(LONGTEXT))
    logic = deferred(Column(LONGTEXT))
    lod = deferred(Column(String(50)))
    topic = Column(String(50))

    spelling_penalty = Column(Float(), nullable=True)

    sections = db.relationship('Section',
                               secondary='question_section')

    choices = relationship('Choice', back_populates='question')
    coding_cases = relationship('CodingCase', back_populates='question')

    question_attempts = relationship("QuestionAttempt",
                                     back_populates="question"
                                     )

    allowed_languages = db.relationship('CodingLanguage',
                                        secondary='question_allowed_languages')

    tags = db.relationship('Tag',
                           secondary='question_tags')

    @staticmethod
    def does_user_have_access(test_id, section_id, question_id, user_id):
        from models import TestAttempt, Test, Section, Choice, QuestionSection

        exists_query = (Question.query
                        .join(QuestionSection)
                        .join(Section)
                        .join(Test)
                        .join(TestAttempt, and_(
                TestAttempt.test_id == Test.id,
                TestAttempt.user_id == user_id,
                TestAttempt.test_id == test_id))
                        .exists())

        exists = db.session.query(exists_query).scalar()

        return exists

    def __str__(self):
        return f"Question ID: {self.id}"
