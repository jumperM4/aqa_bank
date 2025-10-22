from selene import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.support.select import Select

from src.main.ui.Pages.BasePage import BasePage


class DepositPage(BasePage):
    __select_element = s('//select[contains(@class, "account-selector")]')
    __enter_amount_field = s('//input[@placeholder="Enter amount"]')
    __depositBtn = s('//button[text()="💵 Deposit"]')
    __depositPageTitle = s('//h1[text()="💰 Deposit Money"]')

    def chooseSelectElement(self, index_num: int):
        self.__select_element.wait_until(be.visible)
        selected_element = self.__select_element.locate()
        Select(selected_element).select_by_index(index_num)
        return self

    def send_amount_value(self, value: str):
        self.__enter_amount_field.set_value(value)
        return self

    def click_deposit_btn(self):
        self.__depositBtn.click()
        return self

    @property
    def getDepositPageTitle(self):
        self.__depositPageTitle.should(be.visible)
        return self

    def url(self) -> str:
        return "/deposit"

