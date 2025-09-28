from src.main.api.models.base_model import BaseModel
from typing import List


class Transaction(BaseModel):
    id: int
    amount: int
    type: str
    timestamp: str
    relatedAccountId: int


class DepositAccountResponse(BaseModel):
    id: int
    accountNumber: str
    balance: int
    transactions: List[Transaction]
