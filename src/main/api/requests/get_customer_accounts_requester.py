import requests

from src.main.api.models.base_model import BaseModel
from src.main.api.models.get_customer_accounts_response import GetCustomerAccountsResponse
from src.main.api.requests.requester import Requester


class GetCustomerAccountsRequester(Requester):
    def get(self) -> GetCustomerAccountsResponse:
        url = f'{self.base_url}/customer/accounts'
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return GetCustomerAccountsResponse(response.json())

    def post(self, model: BaseModel): ...
