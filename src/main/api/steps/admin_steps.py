from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest):
        create_user_response: CreateUserResponse = ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created(),
            endpoint=Endpoint.ADMIN_CREATE_USER
        ).post(user_request)
        ModelAssertions(user_request, create_user_response).match()

        self.created_objects.append(create_user_response)

        return create_user_response

    def create__invalid_user(self, user_request: CreateUserRequest, error_key: str, error_value: str):
        ValidatedCrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value),
            endpoint=Endpoint.ADMIN_CREATE_USER
        ).post(user_request)

    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_deleted(),
            endpoint=Endpoint.ADMIN_DELETE_USER
        ).delete(user_id)
