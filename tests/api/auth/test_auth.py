import pytest

from assertions.assert_user_contract import assert_user_registered, assert_get_user, assert_user_deleted, \
    assert_user_logged_in, assert_user_logged_out, assert_user_updated, assert_token_refreshed, \
    assert_error_data


class TestAuthApi:
    def test_register_user(self, auth_client, user_credentials):
        resp = auth_client.register(user_credentials)

        body = assert_user_registered(resp)

        access_token = body.access_token

        resp_got = auth_client.get_user(access_token)

        assert_get_user(resp_got)

        resp_delete = auth_client.delete_user(access_token)

        assert_user_deleted(resp_delete)

        resp_got_after_delete = auth_client.get_user(access_token)

        assert resp_got_after_delete.status_code == 404, 'Пользователь не удален'

    def test_get_user(self, auth_client, registered_user):
        access_token = registered_user['access_token']

        resp = auth_client.get_user(access_token)

        assert_get_user(resp)

    def test_login_user(self, auth_client, registered_user):
        payload = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }

        resp = auth_client.login(payload)

        assert_user_logged_in(resp, expected_user=registered_user)

    def test_logout_user(self, auth_client, registered_user):
        access_token = registered_user['access_token']
        refresh_token = registered_user['refresh_token']

        resp = auth_client.logout(refresh_token, access_token)

        assert_user_logged_out(resp)

    def test_update_user(self, auth_client, registered_user):
        access_token = registered_user['access_token']
        payload = {
            'name': f'{registered_user["name"]}_patched',
        }
        resp = auth_client.patch_user(access_token, payload)

        assert_user_updated(resp, expected_user=payload)

    def test_delete_user(self, auth_client, registered_user):
        access_token = registered_user['access_token']

        resp = auth_client.delete_user(access_token)

        assert_user_deleted(resp)

    def test_refresh_token(self, auth_client, registered_user):
        refresh_token = registered_user['refresh_token']

        resp = auth_client.refresh_token(refresh_token)

        assert_token_refreshed(resp)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        'email,password,expected_status',
        [
            ('not-exist@example.com', 'validPass123', 401),
            ('', 'validPass123', 401),
            ('not-exist@example.com', '', 401),
        ],
        ids=['unknown-user', 'empty-email', 'empty-password']
    )
    def test_login_invalid_credentials(self, auth_client, email, password, expected_status):
        resp = auth_client.login({'email': email, 'password': password})

        assert_error_data(resp, expected_status)


@pytest.mark.negative
@pytest.mark.parametrize(
    'method_name,access_token,payload,expected_status,expected_message',
    [
        ('get_user', None, None, 401, 'You should be authorised'),
        ('patch_user', None, {'name': 'patched'}, 401, 'You should be authorised'),
        ('delete_user', None, None, 401, 'You should be authorised'),
    ],
    ids=['get-without-token', 'patch-without-token', 'delete-without-token']
)
def test_protected_methods_without_token(
        auth_client,
        method_name,
        access_token,
        payload,
        expected_status,
        expected_message
):
    assert hasattr(auth_client, method_name), f'Unknown method: {method_name}'
    method = getattr(auth_client, method_name)
    if payload is None:
        resp = method(access_token)
    else:
        resp = method(access_token, payload)

    data = assert_error_data(resp, expected_status)

    assert expected_message in data.message


@pytest.mark.negative
@pytest.mark.parametrize(
    'refresh_token,expected_status',
    [
        ('invalid_refresh_token', 401),
        ('', 401),
        (None, 401),
    ],
    ids=['invalid-token', 'empty-token', 'none-token']
)
def test_refresh_token_invalid_values(
        auth_client,
        refresh_token,
        expected_status
):
    resp = auth_client.refresh_token(refresh_token)
    assert_error_data(resp, expected_status)
