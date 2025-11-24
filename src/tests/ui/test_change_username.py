import allure
import pytest
from selene import browser, be

from src.main.common.storage.SessionStorage import SessionStorage
from src.main.ui.Pages.BankAlerts import BankAlert
from src.main.ui.Pages.EditProfilePage import EditProfilePage
from src.main.ui.Pages.UserDashboard import UserDashboardPage
from src.main.ui.test_data.ui_test_data import UserTestData


class TestUserChangeUsername:
    @pytest.mark.browsers(["chrome"])
    @pytest.mark.usefixtures('setup_user_session')
    @pytest.mark.user_session(count=1)
    @pytest.mark.ui
    def test_user_change_username(self):
        # Получаем первого пользователя из SessionStorage
        user_data = SessionStorage.get_user(0)
        user_steps = SessionStorage.get_steps(0)

        with allure.step("Открыть профиль пользователя"):
            UserDashboardPage().open().clickUserInfo().get_page(page_class=EditProfilePage).getEditProfileTitle.should(
                be.visible)
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Открыта страница редактирования профиля",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Изменить имя пользователя и сохранить"):
            EditProfilePage().sendNewNameValue(
                value=UserTestData.NEW_USERNAME).clickSaveChangesBtn().check_alert_msg_and_accept(
                bank_alert=BankAlert.USERNAME_UPDATED_SUCCESSFULLY)
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Имя пользователя изменено и сохранено",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Обновить страницу после сохранения имени"):
            browser.driver.refresh()
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Страница после рефреша",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Проверить, что имя в UI изменилось"):
            new_name = EditProfilePage().getUsername()
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="UI: имя пользователя изменилось",
                attachment_type=allure.attachment_type.PNG,
            )
            assert new_name == UserTestData.NEW_USERNAME

        # Изменение имени на API
        get_customer_profile_response = user_steps.get_customer_profile(
            create_user_request=user_data,
            new_name=UserTestData.NEW_USERNAME
        )

    @pytest.mark.browsers(["chrome"])
    @pytest.mark.usefixtures('setup_user_session')
    @pytest.mark.user_session(count=1)
    @pytest.mark.ui
    def test_user_change_username_empty_value(self):
        # Получаем первого пользователя из SessionStorage
        user_data = SessionStorage.get_user(0)
        user_steps = SessionStorage.get_steps(0)

        with allure.step("Открыть профиль пользователя"):
            (UserDashboardPage()
             .open()
             .clickUserInfo()
             .get_page(page_class=EditProfilePage)
             .getEditProfileTitle.should(be.visible)
             )
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Открыта страница редактирования профиля",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Проверить и принять алерт при сохранении пустого имени"):
            EditProfilePage().clickSaveChangesBtn().check_alert_msg_and_accept(
                bank_alert=BankAlert.USERNAME_FIELD_REQUIRES_VALID_NAME)
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Алерт на пустое имя",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Обновить страницу после алерта"):
            browser.driver.refresh()
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="Страница после рефреша",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Проверить, что имя в UI не изменилось"):
            new_name = EditProfilePage().getUsername()
            allure.attach(
                browser.driver.get_screenshot_as_png(),
                name="UI: имя не изменилось",
                attachment_type=allure.attachment_type.PNG,
            )
            assert new_name == "Noname"

        # Проверка изменения имени на API
        get_customer_profile_response = user_steps.get_customer_profile_no_asserts(
            create_user_request=user_data
        )

        assert get_customer_profile_response.name is None
