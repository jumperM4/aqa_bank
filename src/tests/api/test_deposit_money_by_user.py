import requests
import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestDepositMoney:
    @pytest.mark.parametrize(
        argnames='balance',
        argvalues=[
            (100)
        ])
    def test_deposit_money(self, balance: int):
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
        # Создание аккаунта
        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response.balance == 0
        assert not create_account_response.transactions
        #
        # Депозит аккаунта
        deposit_account_request = DepositAccountRequest(id=create_account_response.id, balance=balance)

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(deposit_account_request=deposit_account_request)

        assert deposit_account_response.id == create_account_response.id
        assert deposit_account_response.balance == balance
        assert deposit_account_response.transactions
        assert deposit_account_response.transactions[0].amount == balance
        assert deposit_account_response.transactions[0].type == 'DEPOSIT'

        # # Удаление пользователя
        # AdminUserRequester(
        #     request_spec=RequestSpecs.admin_auth_spec(),
        #     response_spec=ResponseSpecs.entity_was_deleted()
        # ).delete(id=create_user_response.id)
