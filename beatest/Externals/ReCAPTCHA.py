"""
ReCAPTCHA Wrappers.

This mainly just requests the ReCaptcha servers to check
if the provided token was valid or not.
"""
import requests
from flask import current_app


class ReCAPTCHA:
    """
    A wrapper class to handle all things related to ReCAPTCHA.
    """

    @staticmethod
    def validate(validation_token):
        """
        Request Google and check if the captcha code was valid or not.

        :param validation_token: the validation token from the client
        :return: None.
                If any errors occurred during validation, this method will
                throw an error
        """
        response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    'secret': current_app.config['RECAPTCHA_SECRET'],
                    'response': validation_token}
        ).json()

        if response['success']:
            return

        raise ValueError("token was not validated")
