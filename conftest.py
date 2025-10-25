from typing import Tuple

from src.main.api.fixtures.user_fixtures import *
from src.main.api.fixtures.api_fixtures import *
from src.main.api.fixtures.objects_fixtures import *

import pytest
from selenium import webdriver
from selene import browser
from src.main.api.configs.config import Config
from src.main.api.steps.admin_steps import AdminSteps
from src.main.common.storage.SessionStorage import SessionStorage
from src.tests.ui.BaseUiTest import BaseUiTest


@pytest.fixture(scope='function')
def setup_selenoid():
    print("setup_selenoid")
    """Настройка браузера через Selenoid"""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    options.set_capability('selenoid:options', {
        'enableVNC': True,
        'enableLog': True,
        'name': 'Selene test run',
    })

    # Конфигурация глобального browser
    browser.config.driver_options = options
    browser.config.driver_remote_url = Config.get("ui_remote_url")
    browser.config.base_url = Config.get("ui_base_url")
    browser.config.timeout = 10

    yield browser

    browser.quit()


@pytest.fixture
def created_user() -> Tuple:
    print("created_user")
    """Создает пользователя через API"""
    user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
    return user_data, new_user


@pytest.fixture
def authenticated_user(setup_selenoid, created_user) -> Tuple:
    print("authenticated_user")
    """Выполняет логин созданного пользователя"""
    user_data, new_user = created_user
    BaseUiTest().authAsUser(username=user_data.username, password=user_data.password)
    return user_data, new_user


@pytest.fixture(autouse=True)
def setup_user_session(request):
    """
    Автоматически выполняется только для тестов с маркером @pytest.mark.user_session.
    НЕ выполняется для тестов, использующих authenticated_user или created_user.
    """
    # Получаем маркер user_session
    marker = request.node.get_closest_marker('user_session')

    # ВАЖНО: Выполняем только если есть маркер И тест не использует authenticated_user
    if marker is not None:
        # Проверяем, использует ли тест authenticated_user или created_user
        test_fixtures = request.fixturenames

        if 'authenticated_user' in test_fixtures or 'created_user' in test_fixtures:
            # Если тест использует эти fixtures, пропускаем setup_user_session
            yield
            return

        # Получаем количество пользователей из маркера
        user_count = marker.kwargs.get('count', 1)

        # Убедимся, что setup_selenoid выполнился
        browser_fixture = request.getfixturevalue('setup_selenoid')

        # Очищаем хранилище перед каждым тестом
        SessionStorage.clear()

        # Создаем список пользователей
        users: List[CreateUserRequest] = []

        for i in range(user_count):
            user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
            new_user = AdminSteps(created_objects=[]).create_user(user_request=user_data)
            users.append(user_data)

        # Добавляем пользователей в SessionStorage
        SessionStorage.add_users(users)

        # Логиним первого пользователя
        if user_count > 0:
            first_user = SessionStorage.get_user(0)
            BaseUiTest().authAsUser(username=first_user.username, password=first_user.password)

    yield

    # Teardown: очищаем после теста (опционально)
    # SessionStorage.clear()