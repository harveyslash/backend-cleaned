from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, \
    Sequence, String, and_
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import deferred, relationship

from Sugar import Dictifiable
from extensions import db


class Test(Dictifiable, db.Model):
    __tablename__ = 'test'

    id = Column(Integer, Sequence('test_id_seq'), primary_key=True)
    leaderboard_id = Column(Integer, ForeignKey('leaderboard.id'))
    name = Column(String(50))
    created_date = Column(DateTime)
    is_active = Column(Boolean)
    type = Column(String(50))  # todo convert to enum
    character = Column(String(50))  # todo convert to enum
    allow_section_jumps = Column(Boolean, nullable=False, default=True)
    price = Column(Integer)
    instruction_html = deferred(Column(LONGTEXT))
    logo = Column(String(500))

    sections = relationship("Section", back_populates="test")
    leaderboard = relationship("Leaderboard", back_populates="tests")
    test_attempts = relationship("TestAttempt", back_populates="test")
    payments = relationship("Payments", back_populates="test")
    college_tests = relationship("CollegeTest", back_populates='test')

    packages = relationship("TestPackage")

    orders = relationship("Order", secondary='order_test',
                          back_populates='tests')

    tests = relationship("Corporate", secondary='corporate_test',
                         back_populates='tests')

    @staticmethod
    def user_has_access(user, test_id: int):
        """
        Check if a User has access to a test.
        A user can access to a test if either:
        1. user has made a payment which was successful
        2. the test is free
        3. the test is free for his college


        :param user: a user object to check for
        :param test_id: the test id to check for
        :return: True , if either of the 2 conditions are true, else False
        """
        from models import Order, OrderTest, CollegeTest

        user_payments_exists = (db
                                .session
                                .query(Order
                                       .query
                                       .filter(Order.user_id == user.id)
                                       .join(OrderTest,
                                             and_(OrderTest.order_id ==
                                                  Order.id,
                                                  OrderTest.test_id == test_id))
                                       .filter(Order.status == "paid")
                                       .exists()
                                       )
                                .scalar())

        if user_payments_exists: return True

        is_test_free = (db
                        .session
                        .query(Test.query
                               .filter(Test.id == test_id)
                               .filter(Test.price == 0)
                               .exists())
                        .scalar())
        if is_test_free: return True

        is_free_for_college = (db.session
                               .query(
                CollegeTest.query
                    .filter(CollegeTest.test_id)
                    .filter(CollegeTest.college_id == user.college_id)
                    .filter(CollegeTest.is_free == True)
                    .exists()
        ).scalar())

        if is_free_for_college: return True

        return False

    @staticmethod
    def test_has_section(test_id: int, section_id: int):
        from models import Section
        test_has_section = (db
                            .session
                            .query(Test.
                                   query
                                   .join(Section)
                                   .filter(Test.id == test_id)
                                   .filter(Section.id == section_id)
                                   .exists())
                            .scalar())

        return test_has_section

    def __str__(self):
        return "id : {}, Name :{}".format(self.id, self.name)
