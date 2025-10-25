from src.main.api.models.base_model import BaseModel
from src.main.api.generators.generating_rule import GeneratingRule
from typing import Annotated


class DepositAccountRequest(BaseModel):
    id: int
    balance: Annotated[int, GeneratingRule(regex=r'[1-9]|[1-9]\d{1,2}|[1-4]\d{3}|5000')]
