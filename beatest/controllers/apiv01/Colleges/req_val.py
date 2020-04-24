"""
Request Validation for Colleges.
Meant to be used by the controllers for Colleges endpoints.

The name is req_val to maintain readability
"""
__author__ = 'Swapnil Dey'

from schematics.models import Model
from schematics.types import IntType, StringType


class CollegeInputs(Model):
    college_name = IntType(required=True)

    college_logo = StringType(required=True)
