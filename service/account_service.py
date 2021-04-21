from repository.account_dao_impl import AccountDAOImpl
from exceptions.resource_unavailable import ResourceUnavailable

from models.client import Client
from flask import jsonify, request


class AccountService:
    account_dao = AccountDAOImpl()

    @classmethod
    def create_account(cls, account):
        return cls.account_dao.create_account(account)

    @classmethod
    def all_accounts(cls, client):
        return cls.account_dao.all_accounts(client)

    @classmethod
    def get_account_by_id(cls, account_id):
        return cls.account_dao.get_account(account_id)

    @classmethod
    def update_account(cls, account):
        return cls.account_dao.update_account(account)

    @classmethod
    def delete_account(cls, account_id):
        return cls.account_dao.delete_account(account_id)

    @classmethod
    def deposit_account(cls, account_id):
        amount = request.json['amount']
        account = cls.account_dao.get_account(account_id)
        if account.balance >= 0:
            account.balance += amount
            cls.account_dao.update_account(account)
            return account.balance

    @classmethod
    def withdraw_account(cls, account_id):
        amount = request.json['amount']
        account = cls.account_dao.get_account(account_id)
        if account.balance >= 0 and amount < account.balance:
            account.balance -= amount
            cls.account_dao.update_account(account)
            return account.balance
        elif amount > account.balance:
            raise ResourceUnavailable(f"You can not withdraw a negative value")

    @classmethod
    def transfer_money(cls, account_id, account_id2):
        amount = request.json['amount']
        account = cls.account_dao.get_account(account_id)
        account2 = cls.account_dao.get_account(account_id2)
        if amount >= 0 and amount < account.balance:
            account.balance -= amount
            account2.balance += amount
            cls.account_dao.update_account(account)
            cls.account_dao.update_account(account2)
        elif amount > account.balance:
            raise ResourceUnavailable(f"You can not withdraw a negative value")
