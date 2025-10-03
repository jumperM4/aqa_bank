from typing import Optional, Union

import requests
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface


class CrudRequester(HttpRequest, CrudEndpointInterface):
    def post (self, model:  BaseModel) -> Response:
        body = model.model_dump() if model is not None else ''

        response = requests.post(
            url=f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def get(self, id: int): ...

    def update(self, model: BaseModel, id: int): ...

    def delete(self, id: int) -> Response:
        response = requests.delete(
            url=f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}/{id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

