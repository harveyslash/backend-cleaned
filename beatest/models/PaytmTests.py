from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class PaytmTests(Dictifiable, db.Model):
    __tablename__ = 'paytm_tests'

    id = Column(Integer, Sequence('paytm_tests_id_seq'), primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'))
    test_ids = Column(String(200))
    transaction_id = Column(String(100))
    transaction_value = Column(String(50))
    tests_activated = Column(Integer)
    promo_code = Column(String(50))

    user = relationship("User", back_populates="paytm_tests")
