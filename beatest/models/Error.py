"""
A model for handling errors responses.
This does not have anything to do with database models.
Instead , it is designed to make error responses to the clien uniform and
predictable.

Example Usage:

Inside a flask endpoint, do:

    return Error(message,http_code,err_code,additional)()  # that () in the end
                                                           # is not a mistake
"""
__author__ = "Harshvardhan Gupta"

from flask import jsonify


class Error(object):
    def __init__(self, message, http_code, err_code=None, additional=None):
        """
        Initialise Error Class
        :param message: the message for the user
        :param http_code: the http code for the response
        :param err_code: the error code for tracking purposes
        :param additional: optional additional messages
        """
        self.message = message
        self.err_code = err_code
        self.additional = additional
        self.http_code = http_code

    def __call__(self, *args, **kwargs):
        response = jsonify({'message': self.message,
                            'error_code': self.err_code,
                            'additional': self.additional})
        response.status_code = self.http_code
        return response
