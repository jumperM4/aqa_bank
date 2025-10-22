import pytest
from selene import browser, be, have, by
from selene.support.shared.jquery_style import s, ss

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.ui.Pages.AdminPanel import AdminPanelPage
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.LoginPage import LoginPage


class TestCreateUser:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_admin_can_create_user(self):
        admin_username, admin_password = CreateUserRequest.getAdmin()
        (LoginPage()
         .open()
         .login(username=admin_username, password=admin_password)
         .get_page(AdminPanelPage)
         .getAdminPanelTitle.should(be.visible))

        new_user: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        ((AdminPanelPage()
         .open()
         .create_user(username=new_user.username, password=new_user.password)
         .check_alert_msg_and_accept(bank_alert=BankAlert.USER_CREATED_SUCCESFULLY))
         .getAllUsers()).element_by(have.text(new_user.username)).should(be.visible)

        # Проверка, что user создался на API
    #
    #
    # @pytest.mark.usefixtures('setup_selenoid')
    # def test_admin_cannot_create_user_with_invalid_data(self):
    #     admin_login = "admin"
    #     admin_password = "admin"
    #
    #     browser.open("/login")
    #     s('[placeholder="Username"]').send_keys(admin_login)
    #     s('[placeholder="Password"]').send_keys(admin_password)
    #     s('.btn-primary').click()
    #
    #     s(by.text("Admin Panel")).should(be.visible)
    #
    #     new_user: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    #     new_user.username = 'abc'
    #
    #     s('[placeholder="Username"]').send_keys(new_user.username)
    #     s('[placeholder="Password"]').send_keys(new_user.password)
    #     s(by.text("Add User")).click()
    #
    #     alert = browser.driver.switch_to.alert
    #     assert alert.text == "Username must be between ..."
    #     alert.accept()
    #
    #     # Проверка, что user НЕ создался на UI
    #     all_users_from_dashboard = ss('//ul//li[contains(@class, "list-group-item")]')
    #     all_users_from_dashboard.element_by(have.text(new_user.username)).should(be.absent)
    #
    #     # Проверка, что user НЕ создался на API