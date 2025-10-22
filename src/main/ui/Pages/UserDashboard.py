from selene.support.shared.jquery_style import s

from src.main.ui.Pages.BasePage import BasePage


class UserDashboardPage(BasePage):
    __userDashboardTitle = s('[@class="welcome-text"]')
    __createNewAccountBtn = s('//button[text()="➕ Create New Account"]')
    __depositBtn = s('//button[text()="💰 Deposit Money"]')
    __makeTransferBtn = s('//button[text()="🔄 Make a Transfer"]')
    __userInfoElement = s('//div[@class="user-info"]')

    def clickUserInfo(self):
        self.__userInfoElement.click()
        return self

    @property
    def getUserDashboardTitle(self):
        return self.__userDashboardTitle

    def url(self) -> str:
        return "/dashboard"

    def createNewAccount(self):
        self.__createNewAccountBtn.click()
        return self

    def depositMoney(self):
        self.__depositBtn.click()
        return self

    def makeTransfer(self):
        self.__makeTransferBtn.click()
        return self
