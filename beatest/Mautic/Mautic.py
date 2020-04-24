from .APINamespace import APINamespace

ACTIVATION_EMAIL_ID = 1


class Mautic:
    """
    All communication sent to CRM is encapsulated in this class.

    This class has two functions:

    1. provide a 1:1 map for raw API
    2. provide higher level functionality that consumes the api
    """
    username = None
    password = None
    url = None
    API = None

    def init_app(self, app):
        self.username = app.config['MAUTIC_USERNAME']
        self.password = app.config['MAUTIC_PASSWORD']
        self.url = app.config['MAUTIC_URL']

        self.API = APINamespace(username=self.username,
                                password=self.password,
                                url=self.url)

    def send_activation_email(self, email, activation_link):
        contacts = self.API.contacts.get_contact_by_email(email)['contacts']
        contact_id = list(contacts.keys())[0]
        contact_id = int(contact_id)

        self.API.contacts.send_email_to_contact(contact_id,
                                                ACTIVATION_EMAIL_ID,
                                                tokens_dict={
                                                    'link': activation_link})
