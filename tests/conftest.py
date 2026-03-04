import pytest
import requests
from faker import Faker

from clients.auth_client import AuthClient
from config import BASE_URL
from utils.requester import CustomRequester


@pytest.fixture(scope='session')
def http_session():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    yield session
    session.close()


@pytest.fixture(scope='session')
def requester(http_session):
    return CustomRequester(session=http_session, base_url=BASE_URL)


@pytest.fixture(scope='session')
def auth_client(requester):
    return AuthClient(requester)


@pytest.fixture(scope='function')
def user_credentials():
    faker = Faker()

    return {
        'email': faker.email(),
        'password': faker.password(),
        'name': faker.name(),
    }


@pytest.fixture(scope='function')
def registered_user(auth_client, user_credentials):
    resp = auth_client.register(user_credentials)

    body = resp.json()

    user_data = {
        'access_token': body.get('accessToken'),
        'refresh_token': body.get('refreshToken'),
        'email': user_credentials.get('email'),
        'password': user_credentials.get('password'),
        'name': user_credentials.get('name'),
    }

    yield user_data

    if user_data.get('access_token'):
        auth_client.delete_user(user_data.get('access_token'))
