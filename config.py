import os

from dotenv import load_dotenv

# Загружаем переменные окружения из .env в корне проекта.
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://stellarburgers.education-services.ru")
