from selene import browser

from src.main.api.specs.request_specs import RequestSpecs


class BaseUiTest:
    def authAsUser(self, username: str, password: str):
        browser.open("/")
        auth_header = RequestSpecs.getUserAuthHeader(username=username, password=password)
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header}');")
