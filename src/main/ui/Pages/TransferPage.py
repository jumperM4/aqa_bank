import time

from selene.support.shared.jquery_style import s, ss
from selenium.webdriver.support.select import Select
from selene import be, browser
from selenium.webdriver.support.wait import WebDriverWait

from src.main.ui.Pages.BasePage import BasePage


class TransferPage(BasePage):
    __select_element = s('//select[contains(@class, "account-selector")]')
    __enterRecipientNameField = s('//input[@placeholder="Enter recipient name"]')
    __enterRecipientAccountNumber = s('//input[@placeholder="Enter recipient account number"]')
    __enterAmount = s('//input[@placeholder="Enter amount"]')
    __confirmCheck = s('//input[@id="confirmCheck"]')
    __sendTransferBtn = s('//button[text()="🚀 Send Transfer"]')
    __transferAgainBtn = s('//button[text()="🔁 Transfer Again"]')
    __repeatTransferBtn = s('//div[text()="🔁 Repeat Transfer"]')
    __elementToRepeat = ss('//li[contains(@class, "list-group-item")]')
    __repeatBtn = './button[text()="🔁 Repeat"]'
    __modalRepeatTransferTitle = s('//div[text()="🔁 Repeat Transfer"]')
    __modal_select_element = s('//select[contains(@class, "form-control")]')
    __modalEnterAmountField = s('//input[@type="number"]')

    def send_enter_amount_field_value(self, value: str):
        self.__modalEnterAmountField.set_value(value)
        return self

    @property
    def getRepeatTransferModalTitle(self):
        self.__modalRepeatTransferTitle.should(be.visible)
        return self

    def chooseSelectElement(self, index_num: int):
        self.__select_element.wait_until(be.visible)
        select_element = self.__select_element.locate()
        time.sleep(1)
        options = Select(select_element).options
        options[index_num].click()
        return self

    def chooseModalSelectElement(self, index_num: int):
        self.__modal_select_element.wait_until(be.visible)
        select_element = self.__modal_select_element.locate()
        time.sleep(1)
        options = Select(select_element).options
        options[index_num].click()
        return self

    def choosePreviousTransactionsToRepeat(self, index_num: int):
        element = self.__elementToRepeat[index_num]
        element.element(self.__repeatBtn).click()
        return self

    def send_recipient_name_value(self, value: str):
        self.__enterRecipientNameField.set_value(value)
        return self

    def send_recipient_account_number_value(self, value: str):
        self.__enterRecipientAccountNumber.set_value(value)
        return self

    def click_confirm_check(self):
        self.__confirmCheck.click()
        return self

    def send_amount_value(self, value: str):
        self.__enterAmount.set_value(value)
        return self

    def click_send_transfer_btn(self):
        self.__sendTransferBtn.click()
        return self

    def click_transfer_again_btn(self):
        self.__transferAgainBtn.click()
        return self

    def click_repeat_transfer_btn(self):
        self.__repeatTransferBtn.click()
        return self

    def url(self) -> str:
        return "/transfer"

