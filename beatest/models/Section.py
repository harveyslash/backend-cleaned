from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence, String, \
    Boolean
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Section(Dictifiable, db.Model):
    __tablename__ = 'section'

    id = Column(Integer, Sequence('section_id_seq'), primary_key=True)
    test_id = Column(Integer, ForeignKey('test.id'))
    name = Column(String(50))
    created_date = Column(DateTime)
    total_time = Column(Integer)
    should_randomize_questions = Column(Boolean,
                                        nullable=False,
                                        default=False)

    test = relationship("Test", back_populates="sections")

    section_attempts = relationship("SectionAttempt", back_populates="section")

    questions = db.relationship('Question',
                                secondary='question_section')

    def __str__(self):
        return f"TestName:::{self.test.name}\n SectionName:::{self.name}"
