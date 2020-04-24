import json

import requests

from .API import API


class ContactsAPI(API):

    def get_contacts(self):
        return requests.get(f"{self.url}/contacts",
                            headers=self.headers).json()

    def create_contact(self, firstname,
                       lastname,
                       email,
                       college_name,
                       phone,
                       join_date,
                       is_active,
                       **kwargs):
        """

        :param firstname:
        :param lastname:
        :param email:
        :param college_name:
        :param phone:
        :param is_active:
        :return:
        """
        return requests.post(f"{self.url}/contacts/new",
                             headers=self.headers,
                             data=
                             {"firstname": firstname,
                                 "lastname": lastname,
                                 "email": email,
                                 "college_name": college_name,
                                 "phone": phone,
                                 "created_date": join_date,
                                 "is_active": is_active,
                                 **kwargs})

    def merge_anon_contact_with_email(self,
                                      anon_id,
                                      email):
        """
        Merge an anonymous contact id with a real email.

        :param anon_id:  contact_id of anonymous user
        :param email:    email to merge the anonymous user with.
        :return:
        """
        return requests.patch(f"{self.url}/contacts/{anon_id}/edit",
                              headers=self.headers,
                              data=
                              {"email": email})

    def send_email_to_contact(self, contact_id, email_id, tokens_dict):
        resp = requests.post(
                f"{self.url}/emails/{email_id}/contact/{contact_id}/send",
                headers=self.json_headers,
                data=json.dumps({'tokens': tokens_dict}))
        return resp

    def get_contact_by_email(self, email):
        resp = requests.get(f"{self.url}/contacts",
                            headers=self.headers,
                            params={
                                'minimal': True,
                                'limit': 1,
                                'search': email
                            })
        return resp.json()
