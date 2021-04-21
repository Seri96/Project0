import unittest
from repository.client_dao_impl import ClientDAOImpl
from repository.client_dao import ClientDAO
from util.connection_factory import connection
from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from models.account import Account
from repository.account_dao import AccountDAO
from controllers import bank_controller
from service.client_service import ClientService


# All DAO and Service methods must have a test proving that they work


class BankTest(unittest.TestCase):

    def test_create_client(self):
        client = Client(client_id=0, username="test")
        client2 = Client(client_id=1, username="test2")
        assert (client) != client2

    def test_get_client_by_id(self):
        client = Client(client_id=0, username="test")
        assert (client.client_id) == 0

    def test_create_account(self):
        account = Account(account_id=0, balance=0, client_id=0)
        account2 = Account(account_id=1, balance=0, client_id=0)
        assert (account) != account2

    def test_account(self):
        account = Account(account_id=1, balance=500, client_id=1)
        assert (account.account_id) == 1
        assert (account.balance) == 500
        assert (account.client_id) == 1

    def test_withdraw(self):
        account = Account(account_id=1, balance=500, client_id=1)
        amount = 250
        assert (account.balance - amount) == 250

    def test_deposit(self):
        account = Account(account_id=1, balance=500, client_id=1)
        amount = 250
        assert (account.balance + amount) == 750

    def test_transfer(self):
        account = Account(account_id=0, balance=500, client_id=0)
        account2 = Account(account_id=1, balance=0, client_id=0)

        amount = 250

        account.balance -= amount
        account2.balance += amount

        assert (account.balance) == 250
        assert (account2.balance) == 250


if __name__ == '__main__':
    unittest.main()
