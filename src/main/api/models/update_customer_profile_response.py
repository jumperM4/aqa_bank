from typing import List

from src.main.api.models.base_model import BaseModel


class Customer(BaseModel):
    id: int
    username: str
    password: str
    name: str
    role: str
    accounts: List


class UpdateCustomerProfileResponse(BaseModel):
    customer: Customer
    message: str
