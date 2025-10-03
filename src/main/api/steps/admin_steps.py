from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest):
        create_user_response = AdminUserRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_created()
        ).post(create_user_request=user_request)

        assert create_user_response.username == user_request.username
        assert create_user_response.role == user_request.role

        self.created_objects.append(create_user_response)

        return create_user_response

    def create__invalid_user(self, user_request: CreateUserRequest, error_key: str, error_value: str):
        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_bad_request(error_key=error_key, error_value=error_value)
        ).post(user_request)

    def delete_user(self, user_id: int):
        AdminUserRequester(
            request_spec=RequestSpecs.admin_auth_spec(),
            response_spec=ResponseSpecs.entity_was_deleted()
        ).delete(id=user_id)
