import requests

from src.main.api.models.base_model import BaseModel
from src.main.api.models.update_customer_profile_request import UpdateCustomerProfileRequest
from src.main.api.models.update_customer_profile_response import UpdateCustomerProfileResponse
from src.main.api.requests.requester import Requester


class UpdateCustomerProfileRequester(Requester):
    def put(self, update_customer_profile_request: UpdateCustomerProfileRequest) -> UpdateCustomerProfileResponse:
        url = f'{self.base_url}/customer/profile'
        response = requests.put(url=url, json=update_customer_profile_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        return UpdateCustomerProfileResponse(**response.json())

    def post(self, model: BaseModel): ...
