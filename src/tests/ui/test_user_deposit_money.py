import time

import pytest
from selene import browser, be, have, by
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver.support.select import Select

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.admin_steps import AdminSteps


class TestUserDepositMoney:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_deposit_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Депозит
        s('//button[text()="➕ Create New Account"]').click()
        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        acc_number = alert_text.split(":", 1)[1].strip()
        alert.accept()

        s('//button[text()="💰 Deposit Money"]').click()
        select_element = s('//select[contains(@class, "account-selector")]').locate()
        Select(select_element).select_by_index(1)
        s('//input[@placeholder="Enter amount"]').send_keys(10)
        s('//button[text()="💵 Deposit"]').click()

        time.sleep(1)
        alert_2 = browser.driver.switch_to.alert
        alert_text_2 = alert_2.text
        assert "10" and acc_number in alert_text_2

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()
        accounts = get_user_accounts_response.model_dump()
        assert accounts[0]["accountNumber"] == acc_number
        assert accounts[0]["balance"] == 10

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_has_no_account_deposit_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Депозит
        s('//button[text()="💰 Deposit Money"]').click()
        s('//h1[text()="💰 Deposit Money"]').should(be.visible)
        s('//button[text()="💵 Deposit"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Please select an account." in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()
        accounts = get_user_accounts_response.model_dump()
        assert len(accounts) == 0

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_deposit_0_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Депозит
        s('//button[text()="➕ Create New Account"]').click()
        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        acc_number = alert_text.split(":", 1)[1].strip()
        alert.accept()

        s('//button[text()="💰 Deposit Money"]').click()
        select_element = s('//select[contains(@class, "account-selector")]').locate()
        Select(select_element).select_by_index(1)
        s('//button[text()="💵 Deposit"]').click()

        time.sleep(1)
        alert_2 = browser.driver.switch_to.alert
        alert_text_2 = alert_2.text
        assert "Please enter a valid amount." in alert_text_2

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()
        accounts = get_user_accounts_response
        assert accounts.root[0].balance == 0
        assert len(accounts.root[0].transactions) == 0
