"""
Facebook Oauth handler.

This Class is a wrapper around the functions that are required
to validate an access token from the user.

A Facebook access token is valid if:
    1. It was issued to the app that Beatest is issued
    2. No errors occur during validation

In order to validate the access token from User, the class first gets an
App access token for itself (using the get_app_access_token_method).
After that, it proceeds to calling the validation method.


Usage:

    from Externals import FacebookOauth
    fb = FacebookOauth(ACCESS_TOKEN)

    if fb.validate():
        return fb.user_id # will have user id for the token

"""

__author__ = "harshvardhan gupta"

from json import loads
from urllib.request import urlopen

from flask import current_app


class FacebookOauth:
    url = "https://graph.facebook.com/v2.12/debug_token?" \
          "input_token={}&" \
          "access_token={}"

    _access_token_url = "https://graph.facebook.com/v2.12/oauth/access_token" \
                        "?client_id={}&" \
                        "client_secret={}&" \
                        "grant_type=client_credentials"

    def __init__(self, token):
        self._token = token
        self._data = None
        self._user_id = None
        self._app_access_token = None

    def _get_app_access_token(self):
        """
        This method get the app level access token using our app id and app
        secret.

        :return:  None
        """
        self._app_access_token = urlopen(
            self._access_token_url.format(
                current_app.config['FACEBOOK_APP_ID'],
                current_app.config['FACEBOOK_APP_SECRET'])) \
            .read()

        self._app_access_token = loads(self._app_access_token)['access_token']

    def validate(self):
        """
        Validate an app token.

        This method requires an app access token, so it gets it using
        get_app_access_token.
        After that it proceeds to validation using the facebook graph debug api


        :return: If any errors occur, False, otherwise True
        """

        try:
            self._get_app_access_token()

            self._data = urlopen(
                self.url.format(
                    self._token,
                    self._app_access_token)) \
                .read()
            self._data = loads(self._data)

            response_app_id = int(self._data['data']['app_id'])

            if response_app_id != current_app.config["FACEBOOK_APP_ID"]:
                raise Exception

            self._user_id = self._data['data']['user_id']
        except Exception:
            return False
        return True

    @property
    def user_id(self):
        """
        Get the user id for the token.

        :return: user id , if validation was successful
        """
        if not self._user_id:
            raise AttributeError("Token Invalid or validate() not called yet")

        return self._user_id
