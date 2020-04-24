import enum

from sqlalchemy import Column, ForeignKey, Integer

from Sugar import Dictifiable
from extensions import db


class Type(enum.Enum):
    MOCK_TEST = 1
    TOPIC_TEST = 2
    VIDEO = 3


class TestPackage(Dictifiable, db.Model):
    """
    Package_id - FK with Package Table
    test_id - FK with Test table
    """
    __tablename__ = 'test_package'

    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('package.id'))
    test_id = Column(Integer, ForeignKey('test.id'))

    component_type = Column(db.Enum(Type), nullable=False, default=Type.MOCK_TEST)
    component_id = Column(Integer)
