

class Client():

    def __init__(self, client_id=0, username=""):
        self.client_id = client_id
        self.username = username
        self.accounts = []

    def json(self):
        return {
            'clientId': self.client_id,
            'username': self.username,
            'accounts': self.accounts

        }

    @staticmethod
    def json_parse(json):
        client = Client(username=json["username"])
        return client

    def __repr__(self):
        return str(self.json())
