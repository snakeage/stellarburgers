from constants import Auth


class AuthClient:
    def __init__(self, requester):
        self.requester = requester

    def register(self, payload):
        return self.requester.send_request(
            method="POST",
            endpoint=Auth.REGISTER,
            data=payload,
        )

    def login(self, payload):
        return self.requester.send_request(
            method="POST",
            endpoint=Auth.LOGIN,
            data=payload,
        )

    def logout(self, refresh_token, access_token):
        return self.requester.send_request(
            method="POST",
            endpoint=Auth.LOGOUT,
            data={"token": refresh_token},
            headers={
                "Authorization": access_token,
            },
        )

    def refresh_token(self, refresh_token):
        return self.requester.send_request(
            method="POST",
            endpoint=Auth.REFRESH_TOKEN,
            data={"token": refresh_token},
        )

    def get_user(self, access_token):
        return self.requester.send_request(
            method="GET",
            endpoint=Auth.USER,
            headers={
                "Authorization": access_token,
            },
        )

    def patch_user(self, access_token, payload):
        return self.requester.send_request(
            method="PATCH",
            endpoint=Auth.USER,
            data=payload,
            headers={
                "Authorization": access_token,
            },
        )

    def delete_user(self, access_token):
        return self.requester.send_request(
            method="DELETE",
            endpoint=Auth.USER,
            headers={
                "Authorization": access_token,
            },
        )
