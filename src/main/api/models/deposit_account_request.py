from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    id: int
    balance: int
