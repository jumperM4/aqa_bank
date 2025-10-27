from selene.support.shared.jquery_style import s

from src.main.ui.Pages.BasePage import BasePage


class LoginPage(BasePage):

    __login_btn = s('.btn-primary')

    def url(self) -> str:
        return "/login"

    def login(self, username: str, password: str):
        self._usernameInput.set_value(username)
        self._passwordInput.set_value(password)
        self.__login_btn.click()
        return self
