import enum

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from Sugar import Dictifiable
from extensions import db


class PackageTypes(enum.Enum):
    COLLEGE = 1
    CAT = 2
    SBI = 3
    IBPS = 4
    IBPS_RRB = 5


class Package(Dictifiable, db.Model):
    """
    Package Name, Description, Type, Price & is_active - Self explanatory
    link_id - Additional linkage currently only for COLLEGE ID
    """
    __tablename__ = 'package'

    id = Column(Integer, primary_key=True)
    package_name = Column(String(50))
    package_description = Column(String(50))
    package_type = Column(db.Enum(PackageTypes), nullable=False, default=PackageTypes.COLLEGE)
    link_id = Column(Integer)
    price = Column(Integer)
    is_active = Column(Boolean, default=False, nullable=False)

    tests = relationship("TestPackage")

