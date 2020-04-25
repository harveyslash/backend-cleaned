class API:
    """
    Base class for all raw apis.
    This provides headers and urls so that the child classes can use
    them directly
    """

    def __init__(self, base64Creds, url):
        self.base64creds = base64Creds
        self.url = f"{url}/api"

        self.headers = {"Authorization": f"Basic {self.base64creds}",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}

        self.json_headers = {"Authorization": f"Basic {self.base64creds}",
            "Content-Type": "application/json; charset=utf-8"}
