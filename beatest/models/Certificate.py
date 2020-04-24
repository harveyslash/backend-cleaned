__author__ = 'harshvardhan gupta'
from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Sequence,
                        String, UniqueConstraint)
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Certificate(Dictifiable, db.Model):
    __tablename__ = 'certificate'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False,
                     unique=True)

    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'course_id'),)

    user = relationship('User', back_populates='certificates')
    course = relationship('Course', back_populates='')
