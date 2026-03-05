from models.auth_models import RegisterResponse, ErrorResponse


def assert_user_registered(resp):
    assert resp.status_code == 200, resp.text

    parsed = RegisterResponse.model_validate(resp.json())

    assert parsed.success is True
    return parsed


def assert_get_user(resp_got):
    assert resp_got.status_code == 200, resp_got.text

    body = resp_got.json()

    assert 'user' in body, 'Отсутствует поле user в ответе'

    user = body['user']

    assert isinstance(user, dict), 'user должен быть dict'

    for field in ('email', 'name'):
        assert field in user, f'Отсутствует поле {field} в ответе'

    return body


def assert_user_deleted(resp):
    assert resp.status_code == 202, resp.text

    body = resp.json()

    assert body, 'Отсутствует тело ответа'
    assert isinstance(body, dict), 'Тело ответа должно быть dict'

    assert 'success' in body, 'Отсутствует поле success'
    assert body['success'] is True


def assert_user_logged_in(resp, expected_user=None):
    assert resp.status_code == 200, resp.text

    body = resp.json()

    assert body, 'Отсутсвует тело ответа'
    assert isinstance(body, dict), 'Тело ответа должно быть dict'

    for field in ('success', 'user', 'accessToken', 'refreshToken'):
        assert field in body, f'Отсутсвует поле {field} в ответе'

    assert body['success'] is True

    user = body['user']

    assert isinstance(user, dict), 'user должен быть dict'

    for field in ('email', 'name'):
        assert field in user, f'Отсутсвует поле {field} в ответе'

    if expected_user:
        assert user['email'] == expected_user['email']
        assert user['name'] == expected_user['name']


def assert_user_logged_out(resp):
    assert resp.status_code == 200, resp.text

    body = resp.json()

    assert body, 'Отсутсвует тело ответа'
    assert isinstance(body, dict), 'Тело ответа должно быть dict'

    for field in ('success', 'message'):
        assert field in body, f'Отсутсвует поле {field} в ответе'

    assert body['success'] is True


def assert_user_updated(resp, expected_user=None):
    assert resp.status_code == 200, resp.text

    body = resp.json()

    assert body, 'Отсутсвует тело ответа'
    assert isinstance(body, dict), 'Тело ответа должно быть dict'

    for field in ('success', 'user'):
        assert field in body, f'Отсутсвует поле {field} в ответе'

    assert body['success'] is True

    user = body['user']

    assert isinstance(user, dict), 'user должен быть dict'

    for field in ('email', 'name'):
        assert field in user, f'Отсутсвует поле {field} в ответе'

    if expected_user:
        assert user['name'] == expected_user['name']


def assert_token_refreshed(resp):
    assert resp.status_code == 200, resp.text

    body = resp.json()

    assert body, 'Отсутсвует тело ответа'
    assert isinstance(body, dict), 'Тело ответа должно быть dict'

    for field in ('success', 'accessToken', 'refreshToken'):
        assert field in body, f'Отсутсвует поле {field} в ответе'

    assert body['accessToken'].startswith('Bearer ')
    assert isinstance(body['refreshToken'], str)


def assert_error_data(resp, status_code: int):
    assert resp.status_code == status_code, resp.text

    parsed = ErrorResponse.model_validate(resp.json())

    assert parsed.success is False
    return parsed
