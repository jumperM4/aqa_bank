import time
from abc import ABC, abstractmethod
from typing import Self, TypeVar, Type
from selene import browser
from selene.support.shared.jquery_style import s
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.main.ui.Pages.BankAlerts import BankAlert

T = TypeVar('T', bound='BasePage')


class BasePage(ABC):
    _usernameInput = s('[placeholder="Username"]')
    _passwordInput = s('[placeholder="Password"]')

    @abstractmethod
    def url(self) -> str: ...

    def open(self) -> Self:
        browser.open(self.url())
        return self

    def get_page(self, page_class: Type[T]) -> T:
        return page_class()  # Работает: возвращает конкретный тип T

    def check_alert_msg_and_accept(self, bank_alert: BankAlert):
        WebDriverWait(browser.driver, 10).until(EC.alert_is_present())
        alert = browser.driver.switch_to.alert
        text = alert.text

        assert bank_alert.message in text
        alert.accept()
        return self, text

    def get_data_from_alert(self, text: str):
        return text.split(":", 1)[1].strip()
