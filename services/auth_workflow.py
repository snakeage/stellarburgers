from assertions.assert_user_contract import (
    assert_get_user,
    assert_user_logged_in,
    assert_user_registered,
    assert_user_updated,
)
from clients.auth_client import AuthClient
from models.auth_entities import LoginPayload, RegisteredUser, RegisterPayload, UpdateUserPayload
from models.auth_models import GetUserResponse, LoginResponse


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

    def register_update_get(
        self, register_payload: RegisterPayload, update_payload: UpdateUserPayload
    ) -> tuple[RegisteredUser, GetUserResponse]:
        register_resp = self.auth_client.register(register_payload)

        registered_data = assert_user_registered(register_resp)

        registered_user = RegisteredUser(
            access_token=registered_data.access_token,
            refresh_token=registered_data.refresh_token,
            email=register_payload.email,
            password=register_payload.password,
            name=register_payload.name,
        )

        update_resp = self.auth_client.patch_user(registered_user.access_token, update_payload)

        assert_user_updated(update_resp, update_payload)

        got_resp = self.auth_client.get_user(registered_user.access_token)

        updated = assert_get_user(got_resp)

        return registered_user, updated
