"""
Model for tracking files in aws s3.

"""
__author__ = 'harshvardhan gupta'
from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Sequence,
                        String)
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class File(Dictifiable, db.Model):
    __tablename__ = 'file'

    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    s3_link = Column(String(512), nullable=False, unique=True)
    mime_type = Column(String(256), nullable=True)

    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)

    user = relationship('User', back_populates='files')
