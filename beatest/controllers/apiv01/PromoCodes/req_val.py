"""
Request Validation for Users.
Meant to be used by the controllers for Users endpoints.

The name is req_val to maintain readability
"""
__author__ = "Swapnil Dey"

from schematics.models import Model
from schematics.types import IntType, StringType, BooleanType


class PromoCodeInputs(Model):
    promo_code = StringType(required=True)

    promo_value = IntType(required=True)

    promo_max_usage = StringType(required=True)

    promo_valid = BooleanType(required=True)

    promo_multiple_use = BooleanType(required=True)


class PromoCodeUpdateInputs(Model):
    promo_code = StringType()

    promo_value = StringType()

    promo_max_usage = StringType()

    promo_valid = BooleanType()

    promo_multiple_use = BooleanType()
