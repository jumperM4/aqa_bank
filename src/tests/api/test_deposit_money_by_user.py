import requests
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.get_customer_accounts_requester import GetCustomerAccountsRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestDepositMoney:
    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.api
    @pytest.mark.parametrize(
        argnames='balance',
        argvalues=[
            (100)
        ])
    def test_deposit_money(self, balance: int, api_manager: ApiManager, user_request: CreateUserRequest):
        # Создание аккаунта
        create_account_response = api_manager.user_steps.create_account(create_user_request=user_request)
        # Депозит аккаунта
        deposit_account_response = api_manager.user_steps.deposit_account(create_user_request=user_request,
                                                                          create_account_response=create_account_response,
                                                                          balance=balance)
        # Получение аккаунтов пользователя
        get_user_account_response = api_manager.user_steps.get_user_accounts_after_deposit(
            create_user_request=user_request,
            create_account_response=create_account_response,
            balance=balance,
            negative=False
        )

    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.api
    @pytest.mark.parametrize(
        argnames='balance, account_id, error_key, error_value',
        argvalues=[
            (100, 0, "", "Unauthorized access to account"),
            (100, 0.5, "", "Unauthorized access to account"),
            (100, -1, "", "Unauthorized access to account"),
            (0, 1, "", "Invalid account or amount"),
            (-1, 1, "", "Invalid account or amount")
        ])
    def test_deposit_money_negative(self,
                                    api_manager: ApiManager,
                                    user_request: CreateUserRequest,
                                    balance: int,
                                    account_id: [int, float],
                                    error_key: str,
                                    error_value: str):
        # Создание аккаунта
        create_account_response = api_manager.user_steps.create_account(create_user_request=user_request)

        # Депозит аккаунта
        deposit_account_response = api_manager.user_steps.deposit_account_negative(create_user_request=user_request,
                                                                                   account_id=account_id,
                                                                                   balance=balance,
                                                                                   error_key=error_key,
                                                                                   error_value=error_value)
        # Получение аккаунтов пользователя
        get_user_account_response = api_manager.user_steps.get_user_accounts_after_deposit(
            create_user_request=user_request,
            create_account_response=create_account_response,
            balance=balance,
            negative=True
        )
