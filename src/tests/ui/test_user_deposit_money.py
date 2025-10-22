import pytest

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.DepositPage import DepositPage
from src.main.ui.Pages.UserDashboard import UserDashboardPage
from src.tests.ui.BaseUiTest import BaseUiTest


class TestUserDepositMoney:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_deposit_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Процесс депозита
        (UserDashboardPage()
         .open()
         .createNewAccount()
         )
        _, alert_text = UserDashboardPage().check_alert_msg_and_accept(bank_alert=BankAlert.USER_CREATED_ACCOUNT_SUCCESSFULLY)
        acc_number = UserDashboardPage().get_data_from_alert(text=alert_text)

        # deposit page
        ((UserDashboardPage()
          .open()
         .depositMoney()
         .get_page(DepositPage)
         .chooseSelectElement(index_num=1)
         .send_amount_value(value="10")).click_deposit_btn())

        _, alert_text_2 = UserDashboardPage().check_alert_msg_and_accept(bank_alert=BankAlert.USER_DEPOSITED_SUCCESSFULLY)
        assert "10" and acc_number in alert_text_2

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)
        assert get_user_accounts_response[0]["accountNumber"] == acc_number
        assert get_user_accounts_response[0]["balance"] == 10

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_has_no_account_deposit_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Депозит
        (UserDashboardPage()
         .open()
         .depositMoney()
         .get_page(DepositPage)
         .getDepositPageTitle
         .click_deposit_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_DEPOSITED_MONEY_WITH_NO_ACCOUNT)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)
        assert len(get_user_accounts_response) == 0

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_deposit_0_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Депозит
        (UserDashboardPage()
         .open()
         .createNewAccount()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_CREATED_ACCOUNT_SUCCESSFULLY))

        (UserDashboardPage()
         .depositMoney()
         .get_page(DepositPage)
         .chooseSelectElement(index_num=1)
         .click_deposit_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_DEPOSITED_MONEY_WITH_EMPTY_AMOUNT_FIELD))


        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

        assert get_user_accounts_response[0]["balance"] == 0
        assert len(get_user_accounts_response[0]["transactions"]) == 0
