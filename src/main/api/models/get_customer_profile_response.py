from typing import List, Any

from src.main.api.models.base_model import BaseModel

class GetCustomerProfileResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Any
    role: str
    accounts: List
