"""
Payments for tests.

THIS MODEL IS DEPRECATED.

We will use Orders/OrderItems instead
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Payments(Dictifiable, db.Model):
    __tablename__ = 'payments'

    id = Column(Integer, Sequence('payment_id_seq'), primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    testId = Column(Integer, ForeignKey('test.id'))
    paymentId = Column(String(100))
    paymentAmount = Column(Integer)
    paymentPromoCode = Column(String(50))
    paymentSuccess = Column(Boolean)

    user = relationship("User", back_populates="payments")
    test = relationship("Test", back_populates="payments")

