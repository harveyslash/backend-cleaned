"""
OrderCourse model.
This specifies one test that is part of an order.

One course order belongs to 1 Order.
One course order has one Course.

"""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class OrderCourse(Dictifiable, db.Model):
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)
