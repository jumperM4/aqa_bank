import requests

from src.main.api.models.base_model import BaseModel
from src.main.api.models.get_customer_profile_response import GetCustomerProfileResponse
from src.main.api.requests.requester import Requester


class GetCustomerProfileRequester(Requester):
    def get(self) -> GetCustomerProfileResponse:
        url = f'{self.base_url}/customer/profile'
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return GetCustomerProfileResponse(**response.json())

    def post(self, model: BaseModel): ...
