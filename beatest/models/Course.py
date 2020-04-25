from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, \
    Sequence, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class Course(Dictifiable, db.Model):
    __tablename__ = 'course'

    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    name = Column(String(255))
    is_active = Column(Boolean)
    price = Column(Integer)

    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)

    orders = relationship("Order", secondary='order_course',
                          back_populates='courses')
    certificates = relationship("Certificate", back_populates='course')

    @staticmethod
    def get_paid_course_ids(user_id):
        """
        Get all paid course ids for the user.

        :param user_id:
        :return: list of all course ids that user has paid for
        """
        from models import OrderCourse, Order
        from sqlalchemy import and_
        from sqlalchemy.orm import load_only

        courses = (Course.query
                   .options(load_only(Course.id))
                   .join(OrderCourse)
                   .join(Order, and_(Order.id == OrderCourse.order_id,
                                     Order.status == 'paid',
                                     Order.user_id == user_id))
                   .filter(Course.is_active == 1)
                   .all())
        return [course.id for course in courses]

    def __str__(self):
        return "id : {}, Name :{}".format(self.id, self.name)
