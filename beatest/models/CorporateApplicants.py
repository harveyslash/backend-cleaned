import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer

from Sugar import Dictifiable
from extensions import db


class ApplicationStatusTypes(enum.Enum):
    shortlisted = 1
    accepted = 2
    rejected = 3


class CorporateApplicants(Dictifiable, db.Model):
    __tablename__ = 'corporate_applicants'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    corporate_id = Column(Integer, ForeignKey('corporate.id'),
                          primary_key=True)

    type = Column(db.Enum(ApplicationStatusTypes), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="application")

    corporate = db.relationship("Corporate",
                                back_populates="corporate_applicants")
