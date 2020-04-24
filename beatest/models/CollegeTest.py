from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, \
    Sequence, Boolean
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class CollegeTest(Dictifiable, db.Model):
    __tablename__ = 'college_test'

    id = Column(Integer, Sequence('college_test_id_seq'), primary_key=True)

    college_id = Column(Integer, ForeignKey('college.id'), nullable=True)
    test_id = Column(Integer, ForeignKey('test.id'), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, nullable=False, default=False)
    should_override = Column(Boolean, nullable=False, default=False)
    is_free = Column(Boolean, nullable=False, default=False)

    UniqueConstraint(college_id, test_id)

    college = relationship('College', back_populates='college_tests')
    test = relationship('Test', back_populates='college_tests')
