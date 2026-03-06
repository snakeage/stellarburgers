from models.auth_models import (
    ErrorResponse,
    GetUserResponse,
    LoginResponse,
    LogoutResponse,
    RefreshResponse,
    RegisterResponse,
    UpdateUserResponse,
)


def assert_user_registered(resp):
    assert resp.status_code == 200, resp.text

    parsed = RegisterResponse.model_validate(resp.json())

    assert parsed.success is True
    return parsed


def assert_get_user(resp_got):
    assert resp_got.status_code == 200, resp_got.text

    parsed = GetUserResponse.model_validate(resp_got.json())
    assert parsed.success is True
    return parsed


def assert_user_deleted(resp):
    assert resp.status_code == 202, resp.text

    body = resp.json()

    assert body, "Отсутствует тело ответа"
    assert isinstance(body, dict), "Тело ответа должно быть dict"

    assert "success" in body, "Отсутствует поле success"
    assert body["success"] is True


def assert_user_logged_in(resp, expected_user=None):
    assert resp.status_code == 200, resp.text

    parsed = LoginResponse.model_validate(resp.json())

    assert parsed.success is True

    if expected_user is not None:
        assert parsed.user.email == expected_user.email
        assert parsed.user.name == expected_user.name

    return parsed


def assert_user_logged_out(resp):
    assert resp.status_code == 200, resp.text

    parsed = LogoutResponse.model_validate(resp.json())

    assert parsed.success is True
    return parsed


def assert_user_updated(resp, expected_user=None):
    assert resp.status_code == 200, resp.text

    parsed = UpdateUserResponse.model_validate(resp.json())

    assert parsed.success is True

    if expected_user:
        expected_data = expected_user.model_dump(exclude_none=True)
        for field, expected_value in expected_data.items():
            assert getattr(parsed.user, field) == expected_value

    return parsed


def assert_token_refreshed(resp):
    assert resp.status_code == 200, resp.text

    parsed = RefreshResponse.model_validate(resp.json())

    assert parsed.success is True
    assert parsed.access_token.startswith("Bearer ")


def assert_error_data(resp, status_code: int):
    assert resp.status_code == status_code, resp.text

    parsed = ErrorResponse.model_validate(resp.json())

    assert parsed.success is False
    return parsed
