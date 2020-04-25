import base64

from Mautic.API import ContactsAPI


class APINamespace:
    """
    A container to hold all the raw apis for mautic.
    each restful resource can be added here in the init function.

    This class is mainly for ease of readability
    """

    def __init__(self, username, password, url):
        self.__username = username
        self.__password = password
        self.__url = url
        string = f"{username}:{password}"

        self.base64Creds = base64.b64encode(string.encode('utf-8')).decode()

        # add more 'resources' as needed
        self.contacts = ContactsAPI(self.base64Creds, url)
