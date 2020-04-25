import enum
from datetime import datetime
from sqlalchemy.sql import func

from flask_login import UserMixin
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, \
    Integer, Sequence, String, Date
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import deferred, relationship

from Sugar.Dictify import Dictifiable
from extensions import db


class UserTypes(enum.Enum):
    standard = 1
    admin = 2


class User(Dictifiable, db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    full_name = Column(String(50))
    fb_id = Column(String(255), unique=True)
    google_id = Column(String(255), unique=True)
    fb_oauth_token = Column(String(500))
    google_oauth_token = Column(String(500))
    google_token_id = Column(String(4000))
    email = Column(String(50), unique=True)
    password = deferred(Column(String(500)))
    profile_picture = Column(LONGTEXT)
    referral_code = Column(String(50))
    referral_bonus = Column(Integer)
    referral_code_used = Column(String(50))
    wallet = Column(Integer)
    phone_no = Column(BigInteger)
    graduation_date = Column(Date)
    degree = Column(String(255))
    branch = Column(String(255))
    type = Column(db.Enum(UserTypes), nullable=False, default='standard')
    is_active = Column(Boolean, default=False, nullable=False)
    college_id = Column(Integer, ForeignKey('college.id'))
    created_date = Column(DateTime, nullable=False, server_default=func.now())

    performance = relationship("Performance", back_populates="user")
    test_attempts = relationship("TestAttempt", back_populates="user")
    payments = relationship("Payments", back_populates="user")
    paytm_tests = relationship("PaytmTests", back_populates="user")
    college = relationship('College', back_populates='college_users')
    orders = relationship('Order', back_populates='user')
    files = relationship('File', back_populates='user')
    certificates = relationship('Certificate', back_populates='user')

    roles = db.relationship('Role',
                            secondary='user_roles')

    corporate = db.relationship('Corporate', secondary='corporate_admin',
                                uselist=False)

    applicant_for = db.relationship('Corporate',
                                    secondary='corporate_applicants')

    application = db.relationship("CorporateApplicants",
                                  back_populates='user', uselist=False)
