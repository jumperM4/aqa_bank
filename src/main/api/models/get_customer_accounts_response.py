from typing import List

from pydantic import RootModel

from src.main.api.models.base_model import BaseModel


class Transaction(BaseModel):
    id: int
    amount: int
    type: str
    timestamp: str
    relatedAccountId: int


class ModelItem(BaseModel):
    id: int
    accountNumber: str
    balance: int
    transactions: List[Transaction]


class GetCustomerAccountsResponse(RootModel[List[ModelItem]]):
    root: List[ModelItem]
