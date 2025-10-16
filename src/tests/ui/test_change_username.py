import time

import pytest
from selene import browser, be, have, by, query
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver.support.select import Select

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps


class TestUserChangeUsername:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_change_username(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        s('//div[@class="user-info"]').click()
        s('//h1[text()="✏️ Edit Profile"]').should(be.visible)
        s('//input[@placeholder="Enter new name"]').should(be.visible).set_value("NewName")
        s('//button[text()="💾 Save Changes"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Name updated successfully!" in alert_text
        alert.accept()

        browser.driver.refresh()

        #       Проверка что UI изменился
        new_name = s('//span[@class="user-name"]').get(query.text)
        assert new_name == "NewName"

        # Изменение имени на API
        get_customer_profile_response = UserSteps(created_objects=[]).get_customer_profile(
            create_user_request=user_data,
            new_name="NewName"
        )

    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_change_username_empty_value(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        s('//div[@class="user-info"]').click()
        s('//h1[text()="✏️ Edit Profile"]').should(be.visible)
        s('//button[text()="💾 Save Changes"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Please enter a valid name." in alert_text
        alert.accept()

        browser.driver.refresh()

        # Проверка что UI НЕ изменился
        new_name = s('//span[@class="user-name"]').get(query.text)
        assert new_name == "Noname"

        # Проверка изменения имени на API
        get_customer_profile_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_CUSTOMER_PROFILE
        ).get_all()
        assert get_customer_profile_response.name is None
