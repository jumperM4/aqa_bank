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
from src.main.api.steps.user_steps import UserSteps


class TestTransferMoney:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_new_transfer_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=20)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        time.sleep(2)
        select_element = s('//select[contains(@class, "account-selector")]').should(be.visible).locate()
        options = Select(select_element).options
        options[2].click()

        s('//input[@placeholder="Enter recipient name"]').send_keys("Name")
        s('//input[@placeholder="Enter recipient account number"]').send_keys(create_account_response_2.accountNumber)
        s('//input[@placeholder="Enter amount"]').send_keys(10)
        s('//input[@id="confirmCheck"]').click()
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "10" and create_account_response_2.accountNumber in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 10

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 10

    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_again_transfer_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_1,
                                                                                 balance=20)
        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_response = UserSteps(created_objects=[]).transfer_money(create_user_request=user_data,
                                                                        sender_id=create_account_response_1.id,
                                                                        receiver_id=create_account_response_2.id,
                                                                        amount=5,
                                                                        message='Transfer successful')

        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        s('//button[text()="🔁 Transfer Again"]').click()
        ss('//li[contains(@class, "list-group-item")]')[1].element('./button[text()="🔁 Repeat"]').click()

        s('//div[text()="🔁 Repeat Transfer"]').should(be.visible)
        time.sleep(2)
        select_element = s('//select[contains(@class, "form-control")]').should(be.visible).locate()
        options = Select(select_element).options
        options[2].click()

        s('//input[@type="number"]').set_value(5)
        s('//input[@id="confirmCheck"]').click()
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert f"Transfer of $5 successful" in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 5

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 15

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_new_transfer_money_empty_fields(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=20)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Please fill all fields and confirm." in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 0

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 20

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_new_transfer_money_no_confirm_check(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_1,
                                                                                 balance=20)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        time.sleep(2)
        select_element = s('//select[contains(@class, "account-selector")]').should(be.visible).locate()
        options = Select(select_element).options
        options[2].click()

        s('//input[@placeholder="Enter recipient name"]').send_keys("Name")
        s('//input[@placeholder="Enter recipient account number"]').send_keys(create_account_response_2.accountNumber)
        s('//input[@placeholder="Enter amount"]').send_keys(10)
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Please fill all fields and confirm." in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 0

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 20

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_new_transfer_insufficient_funds(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_1,
                                                                                 balance=20)
        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        time.sleep(2)
        select_element = s('//select[contains(@class, "account-selector")]').should(be.visible).locate()
        options = Select(select_element).options
        options[1].click()

        s('//input[@placeholder="Enter recipient name"]').send_keys("Name")
        s('//input[@placeholder="Enter recipient account number"]').send_keys(create_account_response_2.accountNumber)
        s('//input[@placeholder="Enter amount"]').send_keys(10)
        s('//input[@id="confirmCheck"]').click()
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Error: Invalid transfer: insufficient funds or invalid accounts" in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 0

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 20

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_again_transfer_money_empty_amount_field(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        auth_header = RequestSpecs.user_auth_spec(user_data.username, user_data.password)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_1,
                                                                                 balance=20)
        # Перевод с аккаунта номер 1 на аккаунт номер 2
        transfer_money_response = UserSteps(created_objects=[]).transfer_money(create_user_request=user_data,
                                                                               sender_id=create_account_response_1.id,
                                                                               receiver_id=create_account_response_2.id,
                                                                               amount=5,
                                                                               message='Transfer successful')

        # Логин пользователем в UI
        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
        browser.open("/dashboard")

        # Перевод денег
        s('//button[text()="🔄 Make a Transfer"]').click()
        s('//button[text()="🔁 Transfer Again"]').click()
        ss('//li[contains(@class, "list-group-item")]')[1].element('./button[text()="🔁 Repeat"]').click()

        s('//div[text()="🔁 Repeat Transfer"]').should(be.visible)
        time.sleep(2)
        select_element = s('//select[contains(@class, "form-control")]').should(be.visible).locate()
        options = Select(select_element).options
        print(options[1])
        options[1].click()

        s('//input[@type="number"]').set_value(0)
        s('//input[@id="confirmCheck"]').click()
        s('//button[text()="🚀 Send Transfer"]').click()

        time.sleep(1)
        alert = browser.driver.switch_to.alert
        alert_text = alert.text
        assert "Transfer failed: Please try again." in alert_text
        alert.accept()

        # Проверка на уровне API
        get_user_accounts_response = ValidatedCrudRequester(
            request_spec=RequestSpecs.user_auth_spec(username=user_data.username,
                                                     password=user_data.password),
            response_spec=ResponseSpecs.request_returns_ok(),
            endpoint=Endpoint.GET_USER_ACCOUNTS
        ).get_all()

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 5

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 15
