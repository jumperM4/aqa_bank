from enum import Enum

from src.main.api.models.base_model import BaseModel
from dataclasses import dataclass

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.get_customer_accounts_response import GetCustomerAccountsResponse
from src.main.api.models.get_customer_profile_response import GetCustomerProfileResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.models.update_customer_profile_request import UpdateCustomerProfileRequest
from src.main.api.models.update_customer_profile_response import UpdateCustomerProfileResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: BaseModel
    response_model: BaseModel


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url='/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=None
    )

    LOGIN_USER = EndpointConfig(
        url='/auth/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    CREATE_USER_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model=None,
        response_model=CreateAccountResponse
    )

    GET_USER_ACCOUNTS = EndpointConfig(
        url='/customer/accounts',
        request_model=None,
        response_model=GetCustomerAccountsResponse
    )

    DEPOSIT_USER_ACCOUNTS = EndpointConfig(
        url='/accounts/deposit',
        request_model=DepositAccountRequest,
        response_model=DepositAccountResponse
    )

    TRANSFER_MONEY = EndpointConfig(
        url='/accounts/transfer',
        request_model=TransferMoneyRequest,
        response_model=TransferMoneyResponse
    )

    UPDATE_CUSTOMER_PROFILE = EndpointConfig(
        url='/customer/profile',
        request_model=UpdateCustomerProfileRequest,
        response_model=UpdateCustomerProfileResponse
    )

    GET_CUSTOMER_PROFILE = EndpointConfig(
        url='/customer/profile',
        request_model=None,
        response_model=GetCustomerProfileResponse
    )
