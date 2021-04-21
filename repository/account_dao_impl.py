from repository.account_dao import AccountDAO
from util.connection_factory import connection
from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from models.account import Account
from flask import jsonify, request


class AccountDAOImpl(AccountDAO):

    def create_account(self, account):
        sql = "INSERT INTO account VALUES (DEFAULT,%s,%s) RETURNING *"
        cursor = connection.cursor()
        cursor.execute(sql, (account.balance, account.client_id))
        connection.commit()
        record = cursor.fetchone()

        return Account(record[0], record[1])

    @ classmethod
    def get_account(self, account_id):
        sql = "SELECT * FROM account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])

        record = cursor.fetchone()

        if record:
            return Account(record[0], float(record[1]), record[2])
        else:
            raise ResourceNotFound(
                f"Account with ID: {account_id} - Not Found")

    @ classmethod
    def all_accounts(self, client_id):

        amountLessThan = request.args.get('amountLessThan')
        amountGreaterThan = request.args.get('amountGreaterThan')

        if amountLessThan and amountGreaterThan:
            sql = "SELECT * FROM account WHERE (balance BETWEEN %s and %s and client_id = %s) "
            cursor = connection.cursor()
            cursor.execute(sql, (int(amountGreaterThan),
                           int(amountLessThan), client_id))

            records = cursor.fetchall()

            account_list = []

            for record in records:
                account = Account(record[0], float(record[1]), record[2])

                account_list.append(account.json())

            return account_list

        else:
            sql = "SELECT * FROM account where client_id = %s"
            cursor = connection.cursor()
            cursor.execute(sql, (client_id))
            records = cursor.fetchall()

            account_list = []

            for record in records:
                account = Account(record[0], float(record[1]), record[2])

                account_list.append(account.json())

            return account_list

    def update_account(self, change):
        sql = "UPDATE account SET balance = %s WHERE account_id = %s RETURNING *"
        cursor = connection.cursor()
        cursor.execute(sql, (change.balance, change.account_id))
        connection.commit()
        record = cursor.fetchone()

        new_account = Account(record[0], float(record[1]), record[2])

        return new_account

    def delete_account(self, account_id):
        sql = "DELETE FROM account WHERE account_id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
