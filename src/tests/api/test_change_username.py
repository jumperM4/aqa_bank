import requests
import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.update_customer_profile_request import UpdateCustomerProfileRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.update_customer_profile_requester import UpdateCustomerProfileRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestChangeUsername:
    @pytest.mark.parametrize(
        argnames="new_name, message",
        argvalues=[
            ("New Name", "Profile updated successfully")
        ]
    )
    def test_deposit_money(self, new_name: str, message: str):
        # Создание пользователя
        create_user_request = CreateUserRequest(username=RandomData.get_username(),
                                                password=RandomData.get_password(), role="USER")

        create_user_response = AdminUserRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_user_request=create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        # Обновление профиля пользователя
        update_customer_profile_request = UpdateCustomerProfileRequest(name=new_name)

        update_customer_profile_response = UpdateCustomerProfileRequester(
            request_spec=RequestSpecs.user_auth_spec(username=create_user_request.username,
                                                     password=create_user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).put(update_customer_profile_request=update_customer_profile_request)

        assert update_customer_profile_response.customer.username == create_user_request.username
        assert update_customer_profile_response.customer.role == create_user_request.role
        assert update_customer_profile_response.customer.name == new_name
        assert update_customer_profile_response.message == message
