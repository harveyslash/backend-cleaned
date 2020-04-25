"""
Request Validation for Users.
Meant to be used by the controllers for Users endpoints.

The name is req_val to maintain readability
"""
__author__ = "Harshvardhan Gupta"

from schematics.models import Model
from schematics.types import StringType

from Sugar.InputValidators import LowerCaseEmailType, ReCaptchaValidator


class ContactUsInputs(Model):
    name = StringType(required=True)
    email = LowerCaseEmailType(required=True)
    message = StringType(required=True)
    captcha_token = ReCaptchaValidator(required=True)
