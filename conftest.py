from src.main.api.fixtures.user_fixtures import *
from src.main.api.fixtures.api_fixtures import *
from src.main.api.fixtures.objects_fixtures import *

import pytest
from selenium import webdriver
from selene import browser
from src.main.api.configs.config import Config

@pytest.fixture(scope='function', autouse=True)
def setup_selenoid():
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
