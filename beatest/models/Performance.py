from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Performance(Dictifiable, db.Model):
    __tablename__ = 'performance'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    leaderboard_id = Column(Integer, ForeignKey('leaderboard.id'), primary_key=True)
    rank = Column(Integer)

    user = relationship("User", back_populates="performance")
    leaderboard = relationship("Leaderboard", back_populates="performance")