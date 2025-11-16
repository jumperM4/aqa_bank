from typing import Type

from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.get_customer_accounts_response import GetCustomerAccountsResponse
from src.main.api.models.get_customer_profile_response import GetCustomerProfileResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.models.update_customer_profile_request import UpdateCustomerProfileRequest
from src.main.api.models.update_customer_profile_response import UpdateCustomerProfileResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def login(self, create_user_request: CreateUserRequest) -> LoginUserResponse:
        login_request = LoginUserRequest(username=create_user_request.username, password=create_user_request.password)
        login_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.unauth_spec(),
            endpoint=Endpoint.LOGIN_USER,
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(login_request)
        ModelAssertions(login_request, login_response).match()
        return login_response

    def create_account(self, create_user_request: CreateUserRequest) -> CreateAccountResponse:
        create_account_response: CreateAccountResponse = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.entity_was_created(),
            endpoint=Endpoint.CREATE_USER_ACCOUNT
        ).post()

        assert create_account_response.balance == 0
        assert not create_account_response.transactions
        return create_account_response

    def deposit_account(self, create_user_request: CreateUserRequest, create_account_response: CreateAccountResponse, balance: int) -> DepositAccountResponse:
        deposit_account_request = DepositAccountRequest(id=create_account_response.id, balance=balance)
        deposit_account_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.DEPOSIT_USER_ACCOUNTS
        ).post(deposit_account_request)
        ModelAssertions(deposit_account_request, deposit_account_response).match()

        assert deposit_account_response.transactions
        assert deposit_account_response.transactions[0].amount == balance
        assert deposit_account_response.transactions[0].type == 'DEPOSIT'
        return deposit_account_response

    def deposit_account_negative(self,
                                 create_user_request: CreateUserRequest,
                                 account_id: [int, float],
                                 balance: int,
                                 error_key: str,
                                 error_value: str):
        deposit_account_request = DepositAccountRequest(id=account_id, balance=balance)
        ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value),
            endpoint=Endpoint.DEPOSIT_USER_ACCOUNTS
        ).post(deposit_account_request)

    def get_user_accounts_after_deposit(self,
                                        create_user_request: CreateUserRequest,
                                        create_account_response: CreateAccountResponse,
                                        balance: int,
                                        negative: bool) -> GetCustomerAccountsResponse:
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response.accountNumber

        if negative:
            assert get_user_accounts_response.root[0].balance == 0
            assert len(get_user_accounts_response.root[0].transactions) == 0
        else:
            assert get_user_accounts_response.root[0].balance == balance
            assert len(get_user_accounts_response.root[0].transactions) > 0
        return get_user_accounts_response

    def get_user_accounts(self,
                          create_user_request: CreateUserRequest,
                          ) -> GetCustomerAccountsResponse:
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()
        return get_user_accounts_response

    def transfer_money(self, create_user_request: CreateUserRequest, sender_id: int, receiver_id: int, amount: int, message: str) -> \
    Type[TransferMoneyResponse]:
        transfer_money_request = TransferMoneyRequest(senderAccountId=sender_id, receiverAccountId=receiver_id, amount=amount)
        transfer_money_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.TRANSFER_MONEY
        ).post(transfer_money_request)
        ModelAssertions(transfer_money_request, transfer_money_response).match()

        assert transfer_money_response.senderAccountId == sender_id
        assert transfer_money_response.receiverAccountId == receiver_id
        assert transfer_money_response.amount == amount
        assert transfer_money_response.message == message
        return TransferMoneyResponse

    def transfer_money_negative(self,
                                create_user_request: CreateUserRequest,
                                sender_id: int,
                                receiver_id: int,
                                amount: int,
                                error_key: str,
                                error_value: str):
        transfer_money_request = TransferMoneyRequest(senderAccountId=sender_id, receiverAccountId=receiver_id, amount=amount)
        ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value),
            endpoint=Endpoint.TRANSFER_MONEY
        ).post(transfer_money_request)

    def get_user_accounts_after_transfer(self,
                                         create_user_request: CreateUserRequest,
                                         create_account_response_1: CreateAccountResponse,
                                         create_account_response_2: CreateAccountResponse,
                                         amount: int,
                                         balance: int,
                                         negative: bool
                                         ) -> Type[GetCustomerAccountsResponse]:
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_1.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].id == create_account_response_2.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_2.accountNumber

        if negative:
            assert get_user_accounts_response.root[0].balance == 0
            assert len(get_user_accounts_response.root[0].transactions) == 0
            assert get_user_accounts_response.root[1].balance == 0
            assert len(get_user_accounts_response.root[1].transactions) == 0
        else:
            assert get_user_accounts_response.root[0].balance == amount
            assert len(get_user_accounts_response.root[0].transactions) > 0
            assert get_user_accounts_response.root[1].balance == balance - amount
            assert len(get_user_accounts_response.root[1].transactions) > 0

        return GetCustomerAccountsResponse

    def update_customer_profile(self, create_user_request: CreateUserRequest, new_name: str, message: str) -> Type[UpdateCustomerProfileResponse]:
        update_customer_profile_request = UpdateCustomerProfileRequest(name=new_name)
        update_customer_profile_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.UPDATE_CUSTOMER_PROFILE
        ).update(update_customer_profile_request)

        assert update_customer_profile_response.customer.username == create_user_request.username
        assert update_customer_profile_response.customer.role == create_user_request.role
        assert update_customer_profile_response.customer.name == new_name
        assert update_customer_profile_response.message == message
        return UpdateCustomerProfileResponse

    def update_customer_profile_negative(self, user_request: CreateUserRequest, new_name: str, error_key: str, error_value: str):
        update_customer_profile_request = UpdateCustomerProfileRequest(name=new_name)
        ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_request.username,
                                                     password=user_request.password),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value),
            endpoint=Endpoint.UPDATE_CUSTOMER_PROFILE
        ).update(update_customer_profile_request)

    def get_customer_profile(self, create_user_request: CreateUserRequest, new_name: str) -> Type[GetCustomerProfileResponse]:
        get_customer_profile_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_CUSTOMER_PROFILE
        ).get_all()

        assert get_customer_profile_response.name == new_name
        return GetCustomerProfileResponse

    def get_customer_profile_no_asserts(self, create_user_request: CreateUserRequest) -> Type[GetCustomerProfileResponse]:
        get_customer_profile_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_CUSTOMER_PROFILE
        ).get_all()

        return get_customer_profile_response
