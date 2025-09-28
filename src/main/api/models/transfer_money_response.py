from src.main.api.models.base_model import BaseModel


class TransferMoneyResponse(BaseModel):
    senderAccountId: int
    message: str
    amount: int
    receiverAccountId: int

