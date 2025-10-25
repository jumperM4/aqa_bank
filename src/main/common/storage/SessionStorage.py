import threading
from typing import List, Tuple

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.steps.user_steps import UserSteps


class SessionStorage:
    """Thread-safe Singleton для хранения сессий пользователей"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SessionStorage, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Храним список пар (CreateUserRequest, UserSteps)
            self._user_steps_pairs: List[Tuple[CreateUserRequest, UserSteps]] = []

    @staticmethod
    def add_users(users: List[CreateUserRequest]) -> None:
        """Добавляет список пользователей в хранилище с их UserSteps"""
        instance = SessionStorage()
        instance._user_steps_pairs.clear()

        for user in users:
            # Создаем UserSteps для каждого пользователя
            user_steps = UserSteps(created_objects=[])
            # Сохраняем пару (user, user_steps)
            instance._user_steps_pairs.append((user, user_steps))

    @staticmethod
    def get_user(index: int = 0) -> CreateUserRequest:
        """Получает пользователя по индексу"""
        instance = SessionStorage()
        return instance._user_steps_pairs[index][0]  # Возвращаем первый элемент пары

    @staticmethod
    def get_steps(index: int = 0) -> UserSteps:
        """Получает UserSteps для пользователя по индексу"""
        instance = SessionStorage()
        return instance._user_steps_pairs[index][1]  # Возвращаем второй элемент пары

    @staticmethod
    def clear() -> None:
        """Очищает все данные из хранилища"""
        instance = SessionStorage()
        instance._user_steps_pairs.clear()