import requests
import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.get_customer_accounts_requester import GetCustomerAccountsRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.requests.transfer_money_requester import TransferMoneyRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransferMoney:
    @pytest.mark.parametrize(
        argnames='amount, message, balance',
        argvalues=[
            (50, 'Transfer successful', 100)
        ])
    def test_transfer_money(self, amount: int, message: str, balance: int):
        # Создание пользователя
        create_user_request = CreateUserRequest(username=RandomData.get_username(),
                                                password=RandomData.get_password(), role="USER")

        create_user_response = AdminUserRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_user_request=create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        # # Логин пользователя
        # login_user_request = LoginUserRequest(username=create_user_request.username,
        #                                       password=create_user_request.password)
        #
        # login_response = LoginUserRequester(
        #     request_spec=RequestSpecs.unauth_spec(),
        #     response_spec=ResponseSpecs.request_returns_ok()
        # ).post(login_user_request=login_user_request)
        #
        # assert login_response.username == create_user_request.username
        # assert login_response.role == create_user_request.role
        #
        # Создание аккаунта №1
        create_account_response_1 = CreateAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response_1.balance == 0
        assert not create_account_response_1.transactions
        #
        # Создание аккаунта №2
        create_account_response_2 = CreateAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response_2.balance == 0
        assert not create_account_response_2.transactions
        #
        # Депозит аккаунта №1
        deposit_account_request = DepositAccountRequest(id=create_account_response_1.id, balance=balance)

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(deposit_account_request=deposit_account_request)

        assert deposit_account_response.id == create_account_response_1.id
        assert deposit_account_response.balance == balance
        assert deposit_account_response.transactions
        assert deposit_account_response.transactions[0].amount == balance
        assert deposit_account_response.transactions[0].type == 'DEPOSIT'

        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_request = TransferMoneyRequest(
            senderAccountId=create_account_response_1.id,
            receiverAccountId=create_account_response_2.id,
            amount=amount
        )

        transfer_money_response = TransferMoneyRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(transfer_money_request=transfer_money_request)

        assert transfer_money_response.senderAccountId == create_account_response_1.id
        assert transfer_money_response.receiverAccountId == create_account_response_2.id
        assert transfer_money_response.amount == amount
        assert transfer_money_response.message == message

        # Получение аккаунтов пользователя
        get_customer_accounts_response = GetCustomerAccountsRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

        assert get_customer_accounts_response.root[0].id == create_account_response_1.id
        assert get_customer_accounts_response.root[0].accountNumber == create_account_response_1.accountNumber
        assert get_customer_accounts_response.root[0].balance == amount
        assert len(get_customer_accounts_response.root[0].transactions) > 0

        assert get_customer_accounts_response.root[1].id == create_account_response_2.id
        assert get_customer_accounts_response.root[1].accountNumber == create_account_response_2.accountNumber
        assert get_customer_accounts_response.root[1].balance == balance - amount
        assert len(get_customer_accounts_response.root[1].transactions) > 0


    @pytest.mark.parametrize(
        argnames='sender_acc_id, receiver_acc_id, amount, error_key, error_value',
        argvalues=[
            (1, 3, 50, "", "Invalid transfer: insufficient funds or invalid accounts"),
            (1, 3, 5000, "", "Invalid transfer: insufficient funds or invalid accounts")
        ])
    def test_transfer_money_negative(self, sender_acc_id: int, receiver_acc_id: int, amount: int, error_key: str, error_value: str):
        # Создание пользователя
        create_user_request = CreateUserRequest(username=RandomData.get_username(),
                                                password=RandomData.get_password(), role="USER")

        create_user_response = AdminUserRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_user_request=create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        # Создание аккаунта №1
        create_account_response_1 = CreateAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response_1.balance == 0
        assert not create_account_response_1.transactions
        #
        # Создание аккаунта №2
        create_account_response_2 = CreateAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response_2.balance == 0
        assert not create_account_response_2.transactions
        #
        # # Депозит аккаунта №1
        # deposit_account_request = DepositAccountRequest(id=create_account_response_1.id, balance=balance)
        #
        # deposit_account_response = DepositAccountRequester(
        #     request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
        #                                              password=create_user_request.password),
        #     response_spec=ResponseSpecs.request_returns_ok()
        # ).post(deposit_account_request=deposit_account_request)
        #
        # assert deposit_account_response.id == create_account_response_1.id
        # assert deposit_account_response.balance == balance
        # assert deposit_account_response.transactions
        # assert deposit_account_response.transactions[0].amount == balance
        # assert deposit_account_response.transactions[0].type == 'DEPOSIT'

        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_request = TransferMoneyRequest(
            senderAccountId=sender_acc_id,
            receiverAccountId=receiver_acc_id,
            amount=amount
        )

        TransferMoneyRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value)
        ).post(transfer_money_request=transfer_money_request)
