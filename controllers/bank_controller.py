from repository.client_dao_impl import ClientDAOImpl
from flask import jsonify, request
from models.account import Account
from models.client import Client
from exceptions.resource_unavailable import ResourceUnavailable
from exceptions.resource_not_found import ResourceNotFound
from service.client_service import ClientService
from service.account_service import AccountService
from logger import logger


def route(app):

    logger.log()

    # POST /clients => Creates a new client
    # return a 201 status code

    @app.route("/clients", methods=['POST'])
    def post_client():
        client = Client.json_parse(request.json)
        client = ClientService.create_client(client)
        return jsonify(client.json()), 201

    # GET /clients => gets all clients
    # return 200

    @app.route("/clients", methods=['GET'])
    def get_all_client():
        return jsonify(ClientService.all_clients()), 200

    # GET /clients/10 => get client with id of 10
    # return 404 if no such client exist

    @app.route("/clients/<client_id>", methods=['GET'])
    def get_client(client_id):
        try:
            client = ClientService.get_client_by_id(int(client_id))
            return jsonify(client.json()), 200
        except ValueError:
            return "Not a valid ID", 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    # PUT /clients/12 => updates client with id of 12
    # return 404 if no such client exist

    @app.route("/clients/<client_id>", methods=['PUT'])
    def put_client(client_id):
        try:
            client = Client.json_parse(request.json)
            client.client_id = int(client_id)
            client = ClientService.update_client(client)
            return jsonify(client.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

    # DELETE /clients/15 => deletes client with the id of15
    # return 404 if no such client exist
    # return 205 if success

    @app.route("/clients/<client_id>", methods=['DELETE'])
    def delete_client(client_id):
        try:
            ClientService.get_client_by_id(int(client_id))
            ClientService.delete_client(int(client_id))
            return 'Successfully Deleted', 205
        except ResourceNotFound as r:
            return r.message, 404

    # POST /clients/5/accounts =>creates a new account for client with the id of 5
    # return a 201 status code

    @app.route("/clients/<client_id>/accounts", methods=['POST'])
    def post_account(client_id):
        account = Account.json_parse(request.json)
        account.client_id = client_id
        account = AccountService.create_account(account)
        return jsonify(account.json()), 201

    # GET /clients/7/accounts => get all accounts for client 7
    # return 404 if no client exists

    # GET /clients/7/accounts?amountLessThan=2000&amountGreaterThan400 => get all accounts for client 7 between 400 and 2000
    # return 404 if no client exists

    @app.route("/clients/<client_id>/accounts", methods=['GET'])
    def get_all_account(client_id):
        try:
            ClientService.get_client_by_id(int(client_id))
            return jsonify(AccountService.all_accounts(client_id)), 200
        except ResourceNotFound as r:
            return r.message, 404

    # GET /clients/9/accounts/4 => get account 4 for client 9
    # return 404 if no account or client exists

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=['GET'])
    def get_client_account_id(client_id, account_id):
        try:
            client_id = ClientService.get_client_by_id(int(client_id))
            account = AccountService.get_account_by_id(int(account_id))

            return jsonify(account.json()), 200
        except ValueError:
            return "Not a valid ID", 400  # Bad Request
        except ResourceNotFound as r:
            return r.message, 404

    # PUT /clients/10/accounts/3 => update account with the id 3 for client 10
    # return 404 if no account or client exists

    @ app.route("/clients/<client_id>/accounts/<account_id>", methods=['PUT'])
    def put_client_account_id(client_id, account_id):
        try:
            client_id = ClientService.get_client_by_id(int(client_id))
            AccountService.get_account_by_id(int(account_id))

            account = Account.json_parse(request.json)
            account.client_id = client_id

            account.account_id = int(account_id)
            account = AccountService.update_account(account)
            return jsonify(account.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

    # DELETE /clients/15/accounts/6 => delete account 6 for client 15
    # return 404 if no account or client exists

    @ app.route("/clients/<client_id>/accounts/<account_id>", methods=['DELETE'])
    def delete_client_account_id(client_id, account_id):
        try:
            ClientService.get_client_by_id(int(client_id))
            AccountService.get_account_by_id(int(account_id))

            AccountService.delete_account(int(account_id))
            return 'Successfully Deleted', 205
        except ResourceNotFound as r:
            return r.message, 404

    # PATCH /clients/17/accounts/12 => Withdraw/deposit given amount (Body: {"deposit":500} or {"withdraw":250}
    # return 404 if no account or client exists
    # return 422 if insufficient funds

    @ app.route("/clients/<client_id>/accounts/<account_id>", methods=['PATCH'])
    def patch_account(client_id, account_id):

        action = request.json['action']
        if action == 'deposit':
            try:
                ClientService.get_client_by_id(int(client_id))
                AccountService.get_account_by_id(int(account_id))

                balance = AccountService.deposit_account(int(account_id))
                return (f'Successfully deposited! New balance is: {balance}'), 200
            except ResourceNotFound as r:
                return r.message, 404

        elif action == 'withdraw':
            try:
                balance = AccountService.withdraw_account(int(account_id))
                return (f'Successfully withdrawn! New balance is: {balance}'), 200
            except ResourceUnavailable as e:
                return e.message, 422
            except ResourceNotFound as r:
                return r.message, 404

    # PATCH /clients/12/accounts/7/transfer/8 => transfer funds from account 7 to account 8 (Body: {"amount":500})
    # return 404 if no client or either account exists
    # return 422 if insufficient funds

    @ app.route("/clients/<client_id>/accounts/<account_id>/transfer/<account_id2>", methods=['PATCH'])
    def transfer_account(client_id, account_id, account_id2):
        action = request.json['action']
        if action == 'transfer':
            try:
                ClientService.get_client_by_id(int(client_id))
                account = AccountService.get_account_by_id(int(account_id))
                account2 = AccountService.get_account_by_id(int(account_id2))

                AccountService.transfer_money(
                    int(account_id), int(account_id2))
                return (f'Successfully transferred! First Account new balance: {account.balance} Second Account new balance: {account2.balance}'), 200

            except ResourceUnavailable as e:
                return e.message, 422
            except ResourceNotFound as r:
                return r.message, 404
