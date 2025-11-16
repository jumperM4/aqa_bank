import os
from pathlib import Path
from typing import Any


class Config:
    _instance = None
    _properties = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config_path = Path(__file__).parents[4] / 'resources' / 'config.properties'
            if not config_path.exists():
                raise ImportError(f'{config_path}: config.properties not found')
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        cls._properties[key] = value
        return cls._instance

    @staticmethod
    def get(key: str, default_value: Any = None) -> Any:
        # ПРИОРИТЕТ 1 - это системное свойство baseApiUrl = BASEAPIURL
        system_value = os.getenv(key)

        if system_value is not None:
            return system_value

        # ПРИОРИТЕТ 2 - это переменная окружения baseApiUrl - BASEAPIURL
        # admin.username -> ADMIN_USERNAME
        env_key = key.replace('.', '_').upper()
        env_value = os.getenv(env_key)

        if env_value is not None:
            return env_value

        # ПРИОРИТЕТ 3 - это config.properties
        return Config()._properties.get(key, default_value)
