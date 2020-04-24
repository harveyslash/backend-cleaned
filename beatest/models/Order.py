"""
Order model.

One user has many orders.
One order can have several 'items'
an item can be of :
    * Test
    * Course
"""
import enum

from sqlalchemy import (Column, String, DECIMAL, ForeignKey, Integer, Sequence,
                        DateTime)
from sqlalchemy.orm import relationship

from Sugar.Dictify import Dictifiable
from extensions import db

from datetime import datetime

__author__ = 'harshvardhan gupta'


class OrderStatusTypes(enum.Enum):
    created = 1
    attempted = 2
    paid = 3,
    cancelled = 4


class Order(Dictifiable, db.Model):
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    rp_order_id = Column(String(255), nullable=True, unique=True)
    status = Column(db.Enum(OrderStatusTypes),
                    default=OrderStatusTypes.created,
                    nullable=False)

    # cost of order minus  promo code (if any)
    amount = Column(DECIMAL(precision=10), nullable=False)

    promo_code_id = Column(ForeignKey('promo_code.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)

    promo_code = relationship('PromoCode', back_populates='orders')
    user = relationship('User', back_populates='orders')
    tests = relationship('Test', secondary='order_test',
                         back_populates='orders')
    courses = relationship('Course', secondary='order_course',
                           back_populates='orders')
