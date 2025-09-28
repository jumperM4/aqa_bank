import logging

import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:

    @staticmethod
    def default_req_headers():
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def unauth_spec():
        return {
            'headers': RequestSpecs.default_req_headers(),
            'base_url': Config.get(key='backendUrl')
        }
    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = 'Basic YWRtaW46YWRtaW4='
        return {
            'headers': headers,
            'base_url': Config.get(key='backendUrl')
        }

    @staticmethod
    def user_auth_spec(username: str, password: str):
        auth_url = f'{Config.get(key="backendUrl")}/auth/login'
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(url=auth_url, json=request.model_dump())
        if response.status_code == 200:
            headers = RequestSpecs.default_req_headers()
            headers['Authorization'] = response.headers.get('Authorization')
            return {
                'headers': headers,
                'base_url': Config.get(key='backendUrl')
            }
        logging.error(f'Authentication failed for {username} with status {response.status_code}')
        raise Exception('Failed to auth user')
