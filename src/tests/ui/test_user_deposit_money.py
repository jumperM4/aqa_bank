import pytest

from src.main.common.storage.SessionStorage import SessionStorage
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.DepositPage import DepositPage
from src.main.ui.Pages.UserDashboard import UserDashboardPage


class TestUserDepositMoney:
    @pytest.mark.browsers(["chrome"])
    @pytest.mark.usefixtures('setup_user_session')
    @pytest.mark.user_session(count=1)
    # @pytest.mark.usefixtures('authenticated_user')
    def test_user_deposit_money(self):
        # Получаем первого пользователя из SessionStorage
        user_data = SessionStorage.get_user(0)
        user_steps = SessionStorage.get_steps(0)
        # user_data, new_user = authenticated_user

        # Генерируем сумму депозита
        deposit_amount: DepositAccountRequest = RandomModelGenerator.generate(DepositAccountRequest)

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
         .send_amount_value(value=deposit_amount.balance)).click_deposit_btn())

        _, alert_text_2 = UserDashboardPage().check_alert_msg_and_accept(bank_alert=BankAlert.USER_DEPOSITED_SUCCESSFULLY)
        assert deposit_amount.balance and acc_number in alert_text_2

        # Проверка на уровне API
        get_user_accounts_response = user_steps.get_user_accounts(create_user_request=user_data)

        assert get_user_accounts_response.root[0].accountNumber == acc_number
        assert get_user_accounts_response.root[0].balance == 10

    @pytest.mark.browsers(["chrome"])
    @pytest.mark.usefixtures('setup_user_session')
    @pytest.mark.user_session(count=1)
    def test_negative_user_has_no_account_deposit_money(self):
        # Получаем первого пользователя из SessionStorage
        user_data = SessionStorage.get_user(0)
        user_steps = SessionStorage.get_steps(0)

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
        get_user_accounts_response = user_steps.get_user_accounts(create_user_request=user_data)
        print(get_user_accounts_response)
        assert len(get_user_accounts_response.root) == 0

    @pytest.mark.browsers(["chrome"])
    @pytest.mark.usefixtures('setup_user_session')
    @pytest.mark.user_session(count=1)
    def test_negative_user_deposit_0_money(self):
        # Получаем первого пользователя из SessionStorage
        user_data = SessionStorage.get_user(0)
        user_steps = SessionStorage.get_steps(0)

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
        get_user_accounts_response = user_steps.get_user_accounts(create_user_request=user_data)

        assert get_user_accounts_response.root[0].balance == 0
        assert len(get_user_accounts_response.root[0].transactions) == 0
