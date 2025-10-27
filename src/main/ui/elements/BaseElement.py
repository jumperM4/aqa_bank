from selene.core.entity import Element, Collection
from selenium.webdriver.common.by import By


class BaseElement:
    # Расширенный базовый класс для Page Object элементов в Selene
    def __init__(self, element: Element):
        self._element = element

    # Поиск элементов
    def find(self, by_selector: str) -> Element:
        # Находит дочерний элемент по селектору
        return self._element.element(by_selector)

    def find_by_css(self, css_selector: str) -> Element:
        # Находит элемент по CSS селектору
        return self._element.element(css_selector)

    def find_by_xpath(self, xpath: str) -> Element:
        # Находит элемент по XPath
        return self._element.element(By.XPATH, xpath)

    def find_all(self, by_selector: str) -> Collection:
        # Находит все дочерние элементы
        return self._element.all(by_selector)

