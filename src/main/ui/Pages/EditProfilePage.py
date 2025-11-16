from selene import be, query
from selene.support.shared.jquery_style import s

from src.main.ui.Pages.BasePage import BasePage


class EditProfilePage(BasePage):
    __editProfileTitle = s('//h1[text()="✏️ Edit Profile"]')
    __enterNewNameField = s('//input[@placeholder="Enter new name"]')
    __saveChangesBtn = s('//button[text()="💾 Save Changes"]')
    __usernameElement = s('//span[@class="user-name"]')

    def getUsername(self):
        username = self.__usernameElement.get(query.text)
        return username

    @property
    def getEditProfileTitle(self):
        return self.__editProfileTitle

    def url(self) -> str:
        return "/edit-profile"

    def sendNewNameValue(self, value: str):
        self.__enterNewNameField.should(be.visible).set_value(value=value)
        return self

    def clickSaveChangesBtn(self):
        self.__saveChangesBtn.click()
        return self
