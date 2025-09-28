from src.main.api.models.base_model import BaseModel


class UpdateCustomerProfileRequest(BaseModel):
    name: str
