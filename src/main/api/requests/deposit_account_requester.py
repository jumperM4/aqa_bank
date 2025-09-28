import requests

from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.requests.requester import Requester


class DepositAccountRequester(Requester):
    def post(self, deposit_account_request: DepositAccountRequest) -> DepositAccountResponse:
        url = f'{self.base_url}/accounts/deposit'
        response = requests.post(url=url, json=deposit_account_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        return DepositAccountResponse(**response.json())
