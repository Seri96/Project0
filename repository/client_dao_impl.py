from repository.client_dao import ClientDAO
from util.connection_factory import connection
from exceptions.resource_not_found import ResourceNotFound
from models.client import Client
from models.account import Account

from repository.account_dao_impl import AccountDAOImpl


class ClientDAOImpl(ClientDAO):

    def create_client(self, client):
        sql = "INSERT INTO client VALUES (DEFAULT,%s ,%s) RETURNING *"
        cursor = connection.cursor()
        cursor.execute(sql, (client.username, client.accounts))
        connection.commit()
        record = cursor.fetchone()

        return Client(record[0], record[1])

    def get_client(self, client_id):
        sql = "SELECT * FROM client where client_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])

        record = cursor.fetchone()

        if record:
            return Client(record[0], record[1])
        else:
            raise ResourceNotFound(f"Client with ID: {client_id} - Not Found")

    def all_client(self):
        sql = "SELECT * FROM client"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        client_list = []

        for record in records:
            accounts = record[2]
            client = Client(record[0], record[1])

            for account in accounts:
                client.accounts.append(AccountDAOImpl.get_account(account))
            client_list.append(client.json())

        return client_list

    def update_client(self, change):
        sql = "UPDATE client SET username = %s WHERE client_id = %s RETURNING *"
        cursor = connection.cursor()
        cursor.execute(sql, (change.username, change.client_id))
        connection.commit()

        record = cursor.fetchone()
        if record:
            return Client(record[0], record[1])
        else:
            raise ResourceNotFound(
                f"Client with ID: {change.client_id} - Not Found")

    def delete_client(self, client_id):
        sql = "DELETE FROM client WHERE client_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        connection.commit()
