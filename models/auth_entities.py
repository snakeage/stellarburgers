from pydantic import EmailStr

from models.base_model import ApiModel


class RegisterPayload(ApiModel):
    email: EmailStr
    password: str
    name: str


class LoginPayload(ApiModel):
    email: EmailStr
    password: str


class UpdateUserPayload(ApiModel):
    email: EmailStr | None = None
    name: str | None = None


class RegisteredUser(ApiModel):
    email: EmailStr
    name: str
    password: str
    access_token: str
    refresh_token: str
