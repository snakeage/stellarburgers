from models.base_model import ApiModel


class UserModel(ApiModel):
    email: str
    name: str


class RegisterResponse(ApiModel):
    success: bool
    access_token: str
    refresh_token: str
    user: UserModel


class ErrorResponse(ApiModel):
    success: bool
    message: str


class LoginResponse(ApiModel):
    success: bool
    access_token: str
    refresh_token: str
    user: UserModel


class UpdateUserResponse(ApiModel):
    success: bool
    user: UserModel


class GetUserResponse(ApiModel):
    success: bool
    user: UserModel


class LogoutResponse(ApiModel):
    success: bool
    message: str


class RefreshResponse(ApiModel):
    success: bool
    access_token: str
    refresh_token: str
