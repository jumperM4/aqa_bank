from selene import query
from selene.core.entity import Element

from src.main.ui.elements.BaseElement import BaseElement


class UserBage(BaseElement):

    def __init__(self, element: Element):
        super().__init__(element)
        # Парсинг сразу в конструкторе
        text_parts = self._element.get(query.text).split('\n')
        self._username = text_parts[0]
        self._role = text_parts[1]

    @property
    def username(self) -> str:
        return self._username

    @property
    def role(self) -> str:
        return self._role
