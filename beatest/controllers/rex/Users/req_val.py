"""
Request Validation for Users.
Meant to be used by the controllers for Users endpoints.

The name is req_val to maintain readability
"""
__author__ = "Harshvardhan Gupta"

from schematics.models import Model
from schematics.types import IntType, StringType

from Sugar.InputValidators import LowerCaseEmailType, ReCaptchaValidator


class LoginInputs(Model):
    email = LowerCaseEmailType(required=True)
    password = StringType(min_length=6, max_length=12, required=True)


class SignupInputs(Model):
    email = LowerCaseEmailType(required=True)
    password = StringType(min_length=6, max_length=12, required=True)
    full_name = StringType(required=True)
    phone_no = IntType(min_value=1000000000, max_value=9999999999,
                       required=True)
    college_id = IntType(min_value=0)
    captcha_token = ReCaptchaValidator(required=True)


class ForgotPasswordInputs(Model):
    email = LowerCaseEmailType(required=True)
    captcha_token = ReCaptchaValidator(required=True)


class ResendActivationInputs(Model):
    email = LowerCaseEmailType(required=True)
    captcha_token = ReCaptchaValidator(required=True)


class ResetPasswordInputs(Model):
    new_password = StringType(min_length=6, max_length=12, required=True)


class ChangePasswordInputs(Model):
    old_password = StringType(min_length=6, max_length=12, required=True)
    new_password = StringType(min_length=6, max_length=12, required=True)
