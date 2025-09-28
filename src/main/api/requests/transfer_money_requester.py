import requests

from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.requests.requester import Requester


class TransferMoneyRequester(Requester):
    def post(self, transfer_money_request: TransferMoneyRequest) -> TransferMoneyResponse:
        url = f'{self.base_url}/accounts/transfer'
        response = requests.post(url=url, json=transfer_money_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        return TransferMoneyResponse(**response.json())
