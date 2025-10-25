import pytest
from selene import browser, be

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.EditProfilePage import EditProfilePage
from src.main.ui.Pages.UserDashboard import UserDashboardPage
from src.main.ui.test_data.ui_test_data import UserTestData
from src.tests.ui.BaseUiTest import BaseUiTest


class TestUserChangeUsername:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_change_username(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        (UserDashboardPage()
         .open()
         .clickUserInfo()
         .get_page(page_class=EditProfilePage)
         .getEditProfileTitle.should(be.visible)
         )

        (EditProfilePage()
         .sendNewNameValue(value=UserTestData.NEW_USERNAME)
         .clickSaveChangesBtn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USERNAME_UPDATED_SUCCESSFULLY)
         )

        browser.driver.refresh()

        # Проверка что UI изменился
        new_name = EditProfilePage().getUsername()
        assert new_name == UserTestData.NEW_USERNAME

        # Изменение имени на API
        get_customer_profile_response = UserSteps(created_objects=[]).get_customer_profile(
            create_user_request=user_data,
            new_name=UserTestData.NEW_USERNAME
        )

    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_change_username_empty_value(self):
        # Создали пользователя
        user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
        # Логин пользователя в UI
        BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)

        (UserDashboardPage()
         .open()
         .clickUserInfo()
         .get_page(page_class=EditProfilePage)
         .getEditProfileTitle.should(be.visible)
         )

        (EditProfilePage()
         .clickSaveChangesBtn()
         .check_alert_msg_and_accept(bank_alert=BankAlert.USERNAME_FIELD_REQUIRES_VALID_NAME)
         )

        browser.driver.refresh()

        # Проверка что UI НЕ изменился
        new_name = EditProfilePage().getUsername()
        assert new_name == "Noname"

        # Проверка изменения имени на API
        get_customer_profile_response = UserSteps(created_objects=[]).get_customer_profile_no_asserts(
            create_user_request=user_data
        )

        assert get_customer_profile_response.name is None
