from uuid import uuid4

import pytest
import requests
from faker import Faker

from clients.auth_client import AuthClient
from config import BASE_URL
from models.auth_entities import RegisteredUser, RegisterPayload
from services.auth_workflow import AuthWorkflow
from utils.requester import CustomRequester


@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    yield session
    session.close()


@pytest.fixture(scope="session")
def requester(http_session):
    return CustomRequester(session=http_session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def auth_client(requester):
    return AuthClient(requester)


@pytest.fixture(scope="function")
def user_credentials():
    faker = Faker()

    return RegisterPayload(
        email=f"aqa_{uuid4().hex[:10]}@example.com",
        password=faker.password(),
        name=faker.name(),
    )


@pytest.fixture(scope="function")
def registered_user(auth_client, user_credentials):
    resp = auth_client.register(user_credentials)

    body = resp.json()

    registered_user = RegisteredUser(
        access_token=body.get("accessToken"),
        refresh_token=body.get("refreshToken"),
        email=user_credentials.email,
        password=user_credentials.password,
        name=user_credentials.name,
    )

    yield registered_user

    if registered_user.access_token:
        auth_client.delete_user(registered_user.access_token)


@pytest.fixture
def auth_workflow(auth_client):
    return AuthWorkflow(auth_client)
