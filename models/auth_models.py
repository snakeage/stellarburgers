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