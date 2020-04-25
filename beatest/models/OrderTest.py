"""
OrderTest model.
This specifies one test that is part of an order.

One test order belongs to 1 Order.
One test order has one Test.

"""
__author = "harshvardhan gupta"

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class OrderTest(Dictifiable, db.Model):
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
    test_id = Column(Integer, ForeignKey("test.id"), primary_key=True)

