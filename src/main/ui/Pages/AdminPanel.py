from selene import by
from selene.support.shared.jquery_style import s, ss

from src.main.ui.Pages.BasePage import BasePage
from src.main.ui.elements.UserBage import UserBage


class AdminPanelPage(BasePage):
    __adminPanelTitle = s(by.text("Admin Panel"))
    __addUserBtn = s(by.text("Add User"))

    @property
    def user_list_items(self):
        """Динамически получает актуальный список пользователей каждый раз"""
        return ss('//ul//li[contains(@class, "list-group-item")]')

    @property
    def getAdminPanelTitle(self):
        return self.__adminPanelTitle

    def url(self) -> str:
        return "/admin"

    def create_user(self, username: str, password: str):
        self._usernameInput.set_value(username)
        self._passwordInput.set_value(password)
        self.__addUserBtn.click()
        return self

    def getAllUsers(self) -> list[UserBage]:
        # Возвращает список всех пользователей как объекты UserBage
        user_elements = self.user_list_items
        # Оборачиваем каждый элемент в UserBage
        return [UserBage(element) for element in user_elements]

    def getUserAt(self, index: int) -> UserBage:
        # Возвращает конкретного пользователя по индексу
        user_elements = self.user_list_items
        user_element = user_elements[index]
        return UserBage(user_element)
