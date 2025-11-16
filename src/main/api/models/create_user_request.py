from typing import Annotated

from src.main.api.configs.config import Config
from src.main.api.generators.generating_rule import GeneratingRule
from src.main.api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: Annotated[str, GeneratingRule(regex="^[A-Za-z0-9]{3,15}$")]
    password: Annotated[str, GeneratingRule(regex="^[A-Z]{3}[a-z]{4}[0-9]{3}[$%&]{2}$")]
    role: Annotated[str, GeneratingRule(regex="^USER$")]

    @staticmethod
    def getAdmin():
        admin_username = Config.get("admin.username")
        admin_password = Config.get("admin.password")
        return admin_username, admin_password
