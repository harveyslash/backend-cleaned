import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer

from Sugar import Dictifiable
from extensions import db


class CorporateTest(Dictifiable, db.Model):
    __tablename__ = 'corporate_test'

    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    corporate_id = Column(Integer, ForeignKey('corporate.id'),
                          primary_key=True)

    date = Column(DateTime, default=datetime.utcnow)
