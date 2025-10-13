import requests
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.update_customer_profile_request import UpdateCustomerProfileRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.get_customer_profile_requester import GetCustomerProfileRequester
from src.main.api.requests.update_customer_profile_requester import UpdateCustomerProfileRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestChangeUsername:
    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.parametrize(
        argnames="new_name, message",
        argvalues=[
            ("New Name", "Profile updated successfully")
        ]
    )
    def test_change_user_info(self, api_manager: ApiManager, user_request: CreateUserRequest, new_name: str, message: str):
        # Обновление профиля пользователя
        update_customer_profile_response = api_manager.user_steps.update_customer_profile(
            create_user_request=user_request,
            new_name=new_name,
            message=message
        )
        # Получение профиля пользователя
        get_customer_profile_response = api_manager.user_steps.get_customer_profile(
            create_user_request=user_request,
            new_name=new_name
        )

    @pytest.mark.usefixtures('api_manager', 'user_request')
    @pytest.mark.parametrize(
        argnames="new_name, error_key, error_value",
        argvalues=[
            ('', "error", "Bad Request")
        ]
    )
    def test_change_user_info_negative(self, api_manager: ApiManager, user_request: CreateUserRequest, new_name, error_key: str, error_value: str):
        # Обновление профиля пользователя
        update_customer_profile_response = api_manager.user_steps.update_customer_profile_negative(
            user_request=user_request,
            new_name=new_name,
            error_key=error_key,
            error_value=error_value
        )
        # Получение профиля пользователя
        get_customer_profile_response = api_manager.user_steps.get_customer_profile(
            create_user_request=user_request,
            new_name=new_name
        )
