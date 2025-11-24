from typing import Optional, TypeVar

import allure
import requests
from requests import Response

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface
from src.main.common.helpers.step_logger import StepLogger

T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):
    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ''
        url = f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}'
        headers = self.request_spec

        def main_action():
            # Вложение запроса
            allure.attach(
                str({'url': url, 'headers': headers, 'body': body}),
                name="Request",
                attachment_type=allure.attachment_type.TEXT
            )
            response = requests.post(url=url, headers=headers, json=body)
            self.response_spec(response)
            # Вложение ответа
            allure.attach(
                str({'status_code': response.status_code, 'body': response.text}),
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )
            return response

        step_title = f'POST request to {self.endpoint.value.url}'
        return StepLogger().log_step(title=step_title, func=main_action)

    def get(self, id: int):
        ...

    def update(self, model: BaseModel, id: int = None):
        body = model.model_dump() if model is not None else ''

        response = requests.put(
            url=f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}',
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)

        return response

    def delete(self, id: int) -> Response:
        response = requests.delete(
            url=f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}/{id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

    def get_all(self) -> Response:
        response = requests.get(
            url=f'{Config.get("server")}{Config.get("api_version")}{self.endpoint.value.url}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
