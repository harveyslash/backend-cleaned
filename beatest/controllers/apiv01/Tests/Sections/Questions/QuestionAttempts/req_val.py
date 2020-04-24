"""
Request Validation for Questions.
Meant to be used by the controllers for Questions endpoints.

The name is req_val to maintain readability
"""
from models.QuestionAttempt import SupportLanguagesEnum

__author__ = "Harshvardhan Gupta"

from schematics import Model
from schematics.types import StringType, IntType, ListType, FloatType
from schematics.exceptions import ValidationError
from models import QuestionAttemptStatusEnum
from schematics.undefined import Undefined
from flask import request


class UpdateQuestionInputs(Model):
    attempt_status = StringType(
            choices=[e.value for e in QuestionAttemptStatusEnum]
    )

    choice_id = IntType(required=False, default=Undefined)

    tita_choice = StringType(required=False, default=Undefined)

    long_answer = StringType(required=False, default=Undefined)

    chosen_language_id = StringType(required=False, default=Undefined)

    def validate_chosen_language_id(self, data, value):

        # remove all the keys that are not present
        # in the request.
        # by default, data will have all keys (if they are not present, they
        # will be set to null)

        keys = [key for key in data.keys()]
        #
        req = request.json
        #

        for key in keys:
            if key not in req:
                if key in data: del data[key]

        # if ("chosen_language_id" in data and "long_answer" not in data) or \
        #         ("long_answer" in data and "chosen_language_id" not in data):
        #     raise ValidationError(
        #             "coding required both coding_language and long_answer to be set")

        if 'choice_id' in data and 'tita_choice' in data:
            raise ValidationError(
                    "choice_id and tita_choice are both sent")


class UpdateQuestionTimeInputs(Model):
    time = FloatType(required=True)





class RunCodeInputs(Model):
    code = StringType(required=True)
    inputs = ListType(StringType)
    language_id = IntType(required=True)
