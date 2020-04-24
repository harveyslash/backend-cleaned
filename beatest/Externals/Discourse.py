"""
Handlers for Discourse.
We require SSO via discourse, so complex logic like signature verification
is handled here.

"""
import base64
import hashlib
import hmac
from urllib import parse

from flask import current_app
from flask_login import current_user
from extensions import celery
import requests


class Discourse:
    @staticmethod
    def _get_key():
        """
        Get the discourse secret in bytes format

        """
        key = bytes(current_app.config['DISCOURSE_SSO_SECRET'],
                    encoding='utf-8')
        return key

    @staticmethod
    def parse_payload(payload, signature):
        """
        Parse the payload and verify the signature using our secret key.

        :param payload: payload from SSO request (sso key)
        :param signature: signature from SSO request (sig key)
        :return: base64 decoded version of the encoded payload.
        """
        try:
            payload = bytes(parse.unquote(payload), encoding='utf-8')
            decoded = base64.decodebytes(payload).decode('utf-8')
            assert 'nonce' in decoded
            assert len(payload) > 0

            key = Discourse._get_key()
            h = hmac.new(key, payload, digestmod=hashlib.sha256)
            this_signature = h.hexdigest()

            if not hmac.compare_digest(this_signature, signature):
                raise ValueError()

            return decoded

        except Exception as e:
            raise ValueError("Invalid Payload")

    @staticmethod
    def prepare_groups(user_id):
        """
        Discourse has an 'add-groups' paramater that specifies which groups
        a user is part of.

        It needs to be a string with comma separated group names.

        :param user_id: the user that the group string should be prepared for
        :return: comma separated string with the format:
                'stucourse-1,stucourse-2,stucourse-3'
        """
        from models import Course
        student_prefix = current_app.config['DISCOURSE_STUDENT_GROUP_FORMAT']
        course_ids = Course.get_paid_course_ids(user_id)
        group_strings = ",".join(
                student_prefix.format(str(course_id)) for course_id in
                    course_ids)
        return group_strings

    @staticmethod
    def build_return_payload(decoded_payload, user_id):
        """
        Discourse requires a return payload with user details and
        signatures.

        :param decoded_payload: the payload that was decoded from parse_payload
        :param user_id: the user to build the payload for
        :return: the query string for discourse URL.
        """
        query_string = parse.parse_qs(decoded_payload)
        params = {
            'nonce': query_string['nonce'][0],
            'email': current_user.email,
            'external_id': current_user.id,
            'add_groups': Discourse.prepare_groups(user_id)
        }

        return_payload = base64.encodebytes(
                bytes(parse.urlencode(params), 'utf-8'))
        key = Discourse._get_key()
        h = hmac.new(key, return_payload, digestmod=hashlib.sha256)

        query_string = parse.urlencode(
                {'sso': return_payload, 'sig': h.hexdigest()})

        return query_string

    @staticmethod
    @celery.task()
    def add_user_to_course(email, course_id):
        """
        Associate a user to a course.
        This will use the discourse api to add the given email to the course id

        **NOTE** the course_id is the id of the course that WE STORE.
                 The course id in the forums will be fetched first.
                 The fetch is done by searching for a group by name:
                 stucourse-{course_id}

        :param email: email for the user
        """
        try:
            response = requests.get(
                    "https://forums.beatest.in/groups/search.json",
                    params={"api_key": current_app.config[
                        "DISCOURSE_API_SECRET"],
                        "api_username": current_app.config[
                            "DISCOURSE_API_USERNAME"
                        ]})

            course_name = current_app.config["DISCOURSE_STUDENT_GROUP_FORMAT"]
            course_name = course_name.format(course_id)
            json_response = response.json()

            discourse_course_id = list(
                    filter(lambda obj: obj["name"] == course_name,
                           json_response))[0]['id']

            requests.put(
                    f"https://forums.beatest.in/groups/{discourse_course_id}/members.json",
                    params={
                        "api_key": current_app.config["DISCOURSE_API_SECRET"],
                        "api_username": current_app.config[
                            "DISCOURSE_API_USERNAME"
                        ]},
                    json={"user_emails": email}
            )
        except:
            pass
