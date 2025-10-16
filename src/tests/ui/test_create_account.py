import pytest
from selene import browser, be, have, by
from selene.support.shared.jquery_style import s, ss

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.specs.request_specs import RequestSpecs


class TestCreateAccount:
    @pytest.mark.usefixtures('setup_selenoid')
    def test_user_can_create_account(self):
        user = AdminSteps.create_user()

        auth_header = RequestSpecs.user_auth_spec(user.username, user.password)

        browser.open("/")
        browser.driver.execute_script(f"window.localStorage.setItem('authToken', '{auth_header['Authorization']}');")
