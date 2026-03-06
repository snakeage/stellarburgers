from assertions.assert_user_contract import assert_user_logged_in, assert_user_registered
from clients.auth_client import AuthClient
from models.auth_entities import LoginPayload, RegisteredUser, RegisterPayload
from models.auth_models import LoginResponse


class AuthWorkflow:
    def __init__(self, auth_client: AuthClient):
        self.auth_client = auth_client

    def register_and_login(
        self, register_payload: RegisterPayload
    ) -> tuple[RegisteredUser, LoginResponse]:
        register_resp = self.auth_client.register(register_payload)

        registered_data = assert_user_registered(register_resp)

        login_payload = LoginPayload(
            email=register_payload.email, password=register_payload.password
        )

        login_resp = self.auth_client.login(login_payload)

        registered_user = RegisteredUser(
            access_token=registered_data.access_token,
            refresh_token=registered_data.refresh_token,
            email=register_payload.email,
            password=register_payload.password,
            name=register_payload.name,
        )

        logged_in = assert_user_logged_in(login_resp, expected_user=registered_user)

        return registered_user, logged_in
