from sqlalchemy import Column, Integer, String

from Sugar import Dictifiable
from extensions import db


class Admin(Dictifiable, db.Model):
    __tablename__ = 'admin'

    email = Column(String(50))
    password = Column(String(50))
    sessionid = Column(Integer, primary_key=True)
