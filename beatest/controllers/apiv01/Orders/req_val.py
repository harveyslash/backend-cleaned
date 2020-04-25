"""
Request Validation for Orders.
Meant to be used by the controllers for Order endpoints.

The name is req_val to maintain readability
"""
from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import IntType, ListType, StringType

__author__ = 'Harshvardhan Gupta'


class OrderCreateInputs(Model):
    tests = ListType(IntType, min_size=1, )
    courses = ListType(IntType, min_size=1, )
    promo_code = StringType()

    def validate_promo_code(self, data, value):
        """
        Since promo code is the last field,
        tests/courses are validated here.

        """
        if data['tests'] is None and data["courses"] is None:
            raise ValidationError("Tests and courses are both absent")
