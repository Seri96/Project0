from models.client import Client


class Account:

    def __init__(self,  account_id=0, balance=0, client_id=0):
        self.balance = balance
        self.account_id = account_id
        self.client_id = client_id

    def json(self):
        return {
            'balance': self.balance,
            'accountId': self.account_id,
            'clientId': self.client_id
        }

    @ staticmethod
    def json_parse(json):
        account = Account(balance=json["balance"])
        return account

    def __repr__(self):
        return str(self.json())
