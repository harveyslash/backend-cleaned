from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from Sugar import Dictifiable
from extensions import db


class CorporateAdmin(Dictifiable, db.Model):
    __tablename__ = 'corporate_admin'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True,
                     unique=True)
    corporate_id = Column(Integer, ForeignKey('corporate.id'),
                          primary_key=True)

    admin = db.relationship('User', backref='corporate_admin')
    corporate = db.relationship('Corporate', backref='corporate_admin')
