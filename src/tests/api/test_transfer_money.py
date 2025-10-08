import requests
import pytest

from src.main.api.classes.api_manager import ApiManager
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
    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.parametrize(
        argnames='amount, message, balance',
        argvalues=[
            (50, 'Transfer successful', 100)
        ])
    def test_transfer_money(self, amount: int, message: str, balance: int, api_manager: ApiManager, user_request: CreateUserRequest):
        # Создание аккаунта №1
        create_account_response_1 = api_manager.user_steps.create_account(create_user_request=user_request)

        # Создание аккаунта №2
        create_account_response_2 = api_manager.user_steps.create_account(create_user_request=user_request)

        # Депозит аккаунта №1
        deposit_account_response = api_manager.user_steps.deposit_account(create_user_request=user_request,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=balance)

        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_response = api_manager.user_steps.transfer_money(create_user_request=user_request,
                                                                        sender_id=create_account_response_1.id,
                                                                        receiver_id=create_account_response_2.id,
                                                                        amount=amount,
                                                                        message=message)

        # Получение аккаунтов пользователя
        get_user_account_response = api_manager.user_steps.get_user_accounts_after_transfer(
            create_user_request=user_request,
            create_account_response_1=create_account_response_1,
            create_account_response_2=create_account_response_2,
            amount=amount,
            balance=balance,
            negative=False)


    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.parametrize(
        argnames='sender_acc_id, receiver_acc_id, amount, balance, error_key, error_value',
        argvalues=[
            (1, 3, 50, 10, "", "Invalid transfer: insufficient funds or invalid accounts"),
            (1, 3, 5000, 10, "", "Invalid transfer: insufficient funds or invalid accounts")
        ])
    def test_transfer_money_negative(self,
                                     api_manager: ApiManager,
                                     user_request: CreateUserRequest,
                                     sender_acc_id: int,
                                     receiver_acc_id: int,
                                     amount: int,
                                     balance: int,
                                     error_key: str,
                                     error_value: str):
        # Создание аккаунта №1
        create_account_response_1 = api_manager.user_steps.create_account(create_user_request=user_request)

        #
        # Создание аккаунта №2
        create_account_response_2 = api_manager.user_steps.create_account(create_user_request=user_request)

        # Депозит аккаунта №1
        deposit_account_response = api_manager.user_steps.deposit_account(create_user_request=user_request,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=balance)

        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_response = api_manager.user_steps.transfer_money_negative(create_user_request=user_request,
                                                                                 sender_id=sender_acc_id,
                                                                                 receiver_id=receiver_acc_id,
                                                                                 amount=amount,
                                                                                 error_key=error_key,
                                                                                 error_value=error_value)

        # Получение аккаунтов пользователя
        get_user_account_response = api_manager.user_steps.get_user_accounts_after_transfer(
            create_user_request=user_request,
            create_account_response_1=create_account_response_1,
            create_account_response_2=create_account_response_2,
            amount=amount,
            balance=balance,
            negative=True)

