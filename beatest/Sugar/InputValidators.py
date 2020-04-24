"""
Additional Input validators for Handling input parsing.

This uses the schematics library

"""
from schematics.exceptions import ValidationError
from schematics.types import EmailType, StringType

from Externals import ReCAPTCHA


class LowerCaseEmailType(EmailType):
    """
    A subclass of Email type , but it converts the input string to
    lower case BEFORE proceeding with usual email validation
    """

    def convert(self, value, context=None):
        value = super().convert(value, context)
        return value.lower()


class CleanedStringType(StringType):
    """
    A string type converter with the added functionality of allowing
    arbitrary transformations on the input.

    Usage :
        my_field = CleanedStringType(converters=[lambda x : x.tolower()])
    """
    converters = []

    def __init__(self, **kwargs):
        """
        This takes in all the inputs as String Type, but takes in an extra
        input called converters.

        Converters must be a list of functions, and each of those functions
        must take in exactly 1 value , and return the transformed input
        :param kwargs:
        """
        if 'converters' in kwargs:
            self.converters = kwargs['converters']
        del kwargs['converters']
        super().__init__(**kwargs)

    def convert(self, value, context=None):
        value = super().convert(value, context)
        for func in self.converters:
            value = func(value)
        return value


class ReCaptchaValidator(StringType):

    def validate(self, value, context=None):
        super().validate(value, context)
        try:
            ReCAPTCHA.validate(value)
        except:
            raise ValidationError("Captcha was not validated")
