"""
Request Validation for Questions.
Meant to be used by the controllers for Questions endpoints.

The name is req_val to maintain readability
"""
__author__ = "Harshvardhan Gupta"

from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import FloatType, IntType, StringType

from Sugar.InputValidators import CleanedStringType


class QuestionInputs(Model):
    html = StringType(required=True)

    points_correct = FloatType(required=True)

    points_wrong = FloatType(required=True)

    rc_passage = StringType()

    tita_answer = StringType()

    choice_id = IntType()

    type = CleanedStringType(required=True, converters=[lambda x: x.upper()])

    logic = StringType(required=True)

    lod = StringType(required=True)

    topic = StringType(required=True)

    def validate_type(self, data, value):

        if data['tita_answer'] is not None and data['choice_id'] is not None:
            raise ValidationError("TITA and choice_id are both non null")

        if value == 'TITA':
            if data['tita_answer'] is None:
                raise ValidationError("TITA Answer not provided for TITA "
                                      "type Question")
        elif value == 'MCQ':
            if data['choice_id'] is None:
                raise ValidationError("Choice id not provided for MCQ type "
                                      "Question")
        else:
            raise ValidationError("Invalid Question Type")
