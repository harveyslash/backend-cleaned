from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class College(Dictifiable, db.Model):
    __tablename__ = 'college'

    id = Column(Integer, Sequence('college_id_seq'), primary_key=True)
    college_name = Column(String(100), unique=True)
    college_logo = Column("college_logo", String(500))
    college_tests = relationship('CollegeTest', back_populates='college')
    college_users = relationship('User', back_populates='college')

