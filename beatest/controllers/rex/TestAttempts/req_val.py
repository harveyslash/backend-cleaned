"""
Request Validation for Users.
Meant to be used by the controllers for Users endpoints.

The name is req_val to maintain readability
"""
from models.CorporateApplicants import ApplicationStatusTypes

__author__ = "Harshvardhan Gupta"

from schematics.models import Model
from schematics.types import IntType, StringType, ListType, FloatType

from Sugar.InputValidators import LowerCaseEmailType, ReCaptchaValidator


class UpdateApplicants(Model):
    user_ids = ListType(IntType, required=True)
    status = StringType(choices=[e.name for e in ApplicationStatusTypes])


class UpdateScore(Model):
    score = FloatType(required=True)
