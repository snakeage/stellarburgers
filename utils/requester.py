import json
import logging
import os

import requests


class CustomRequester:
    """
    Инфраструктурный слой для отправки HTTP-запросов.
    Отвечает только за транспорт:
    - формирование URL
    - отправку запроса
    - логирование
    - возврат response
    """

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method: str,
            endpoint: str,
            data=None,
            params=None,
            headers=None,
            timeout=15,
            need_logging: bool = True,
    ) -> requests.Response:

        url = f'{self.base_url}{endpoint}'

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=headers,
            timeout=timeout,
        )

        if need_logging:
            self.log_request_and_response(response)

        return response

    def log_request_and_response(self, response: requests.Response):

        try:
            request = response.request

            headers = " \\\n".join(
                [f"-H '{h}: {v}'" for h, v in request.headers.items()]
            )

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body:
                if isinstance(request.body, bytes):
                    body_str = request.body.decode("utf-8")
                else:
                    body_str = str(request.body)

                if body_str != "{}":
                    body = f"-d '{body_str}' \n"

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{full_test_name}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text

            try:
                response_data = json.dumps(
                    json.loads(response.text),
                    indent=4,
                    ensure_ascii=False,
                )
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            self.logger.info(
                f"\tSTATUS_CODE: {response.status_code}\n"
                f"\tDATA:\n{response_data}"
            )

            self.logger.info(f"{'=' * 80}\n")

        except Exception as e:
            self.logger.error(f"Logging failed: {type(e)} - {e}")
