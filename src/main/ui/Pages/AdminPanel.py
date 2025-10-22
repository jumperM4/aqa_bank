from selene import by
from selene.support.shared.jquery_style import s, ss

from src.main.ui.Pages.BasePage import BasePage


class AdminPanelPage(BasePage):
    __adminPanelTitle = s(by.text("Admin Panel"))
    __addUserBtn = s(by.text("Add User"))

    @property
    def getAdminPanelTitle(self):
        return self.__adminPanelTitle

    def url(self) -> str:
        return "/admin"

    def create_user(self, username: str, password: str):
        self.__usernameInput.set_value(username)
        self.__passwordInput.set_value(password)
        self.__addUserBtn.click()
        return self

    def getAllUsers(self):
        return ss('//ul//li[contains(@class, "list-group-item")]')
