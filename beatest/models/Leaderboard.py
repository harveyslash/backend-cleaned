from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Leaderboard(Dictifiable, db.Model):
    __tablename__ = 'leaderboard'

    id = Column(Integer, Sequence('leaderboard_id_seq'), primary_key=True)
    name = Column(String(50))

    performance = relationship("Performance", back_populates="leaderboard")
    tests = relationship("Test", back_populates="leaderboard")

