import pytest

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.TransferPage import TransferPage
from src.main.ui.Pages.UserDashboard import UserDashboardPage
from src.tests.ui.BaseUiTest import BaseUiTest


class TestTransferMoney:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_new_transfer_money(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=20)
        # Логин пользователем в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(page_class=TransferPage)
         .chooseSelectElement(index_num=2)
         .send_recipient_name_value(value="Name")
         .send_recipient_account_number_value(value=create_account_response_2.accountNumber)
         .send_amount_value(value=10)
         .click_confirm_check()
         .click_send_transfer_btn()
         )

        _, alert_text = TransferPage().check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_MONEY_SUCCESSFULLY)
        assert "10" and create_account_response_2.accountNumber in alert_text

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

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
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(page_class=TransferPage)
         .click_transfer_again_btn()
         .choosePreviousTransactionsToRepeat(index_num=1)
         .getRepeatTransferModalTitle
         )

        (TransferPage()
         .chooseModalSelectElement(index_num=2)
         .send_enter_amount_field_value(value=5)
         .click_confirm_check()
         .click_send_transfer_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_MONEY_SUCCESSFULLY_AGAIN)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

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

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                          create_account_response=create_account_response_1,
                                                                          balance=20)
        # Логин пользователем в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(TransferPage)
         .click_send_transfer_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_MONEY_WITH_EMPTY_FIELDS)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

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

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_1,
                                                                                 balance=20)
        # Логин пользователем в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(page_class=TransferPage)
         .chooseSelectElement(index_num=2)
         .send_recipient_name_value(value="Name")
         .send_recipient_account_number_value(value=create_account_response_2.accountNumber)
         .send_amount_value(value=10)
         .click_send_transfer_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_MONEY_WITH_FILLED_FIELDS_AND_NO_CONFIRM_CHECK)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

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

        # Создание аккаунта 1
        create_account_response_1 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Создание аккаунта 2
        create_account_response_2 = UserSteps(created_objects=[]).create_account(create_user_request=user_data)
        # Депозит аккаунта №1
        deposit_account_response = UserSteps(created_objects=[]).deposit_account(create_user_request=user_data,
                                                                                 create_account_response=create_account_response_2,
                                                                                 balance=20)
        # Логин пользователем в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(page_class=TransferPage)
         .chooseSelectElement(index_num=1)
         .send_recipient_name_value(value="Name")
         .send_recipient_account_number_value(value=create_account_response_2.accountNumber)
         .send_amount_value(value=10)
         .click_confirm_check()
         .click_send_transfer_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_INSUFFICIENT_FUNDS)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)
        print(get_user_accounts_response.root[0])
        print(get_user_accounts_response.root[1])

        assert get_user_accounts_response.root[0].id == create_account_response_1.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[0].balance == 0

        assert get_user_accounts_response.root[1].id == create_account_response_2.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[1].balance == 20

    @pytest.mark.usefixtures('setup_selenoid')
    def test_negative_user_again_transfer_money_empty_amount_field(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)

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
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        # Перевод денег
        (UserDashboardPage()
         .open()
         .makeTransfer()
         .get_page(page_class=TransferPage)
         .click_transfer_again_btn()
         .choosePreviousTransactionsToRepeat(index_num=1)
         .getRepeatTransferModalTitle
         )

        (TransferPage()
         .chooseModalSelectElement(index_num=1)
         .send_enter_amount_field_value(value=0)
         .click_confirm_check()
         .click_send_transfer_btn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_TRANSFERRED_MONEY_AGAIN_FAILED)
         )

        # Проверка на уровне API
        get_user_accounts_response = UserSteps(created_objects=[]).get_user_accounts(create_user_request=user_data)

        assert get_user_accounts_response.root[0].id == create_account_response_2.id
        assert get_user_accounts_response.root[0].accountNumber == create_account_response_2.accountNumber
        assert get_user_accounts_response.root[0].balance == 5

        assert get_user_accounts_response.root[1].id == create_account_response_1.id
        assert get_user_accounts_response.root[1].accountNumber == create_account_response_1.accountNumber
        assert get_user_accounts_response.root[1].balance == 15
