# AQA Python Project Blueprint (Notion Ready)

> Цель: быстрый и системный вход в AQA Python с архитектурой, которую понимают и в РФ, и в международных командах.

## Как использовать в Notion
1. Import -> Markdown & CSV -> выбрать этот файл.
2. Создать страницу `AQA API Project Blueprint`.
3. Каждый раздел ниже свернуть/развернуть как toggle и проходить по порядку.

---

## 0) Project Setup (Старт за 15 минут)

<details>
<summary><strong>Что делаем</strong></summary>

- Создаём репозиторий и базовую структуру проекта.
- Поднимаем виртуальное окружение.
- Фиксируем зависимости в `requirements.txt`.

</details>

<details>
<summary><strong>Команды</strong></summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

</details>

<details>
<summary><strong>Почему это важно</strong></summary>

- `.venv` изолирует проект от глобального Python.
- Повторяемость: у тебя и у CI одинаковые зависимости.
- Без этого начнется хаос версий и «у меня работает».

</details>

---

## 1) Базовая структура слоёв

<details>
<summary><strong>Создать папки и файлы</strong></summary>

```text
clients/
assertions/
models/
services/
tests/
utils/
config.py
constants.py
pytest.ini
pyproject.toml
.pre-commit-config.yaml
requirements.txt
.gitignore
README.md
```

</details>

<details>
<summary><strong>Зачем каждый слой</strong></summary>

- `clients/`: чистые HTTP-вызовы по endpoint.
- `assertions/`: проверки контрактов и бизнес-ожиданий.
- `models/`: Pydantic-модели запросов/ответов.
- `services/`: workflow (цепочки шагов).
- `tests/`: сценарии (читаемые, короткие).
- `utils/`: транспорт/логирование/вспомогательное.

</details>

---

## 2) Dependencies (минимум и зачем)

<details>
<summary><strong>Установить библиотеки</strong></summary>

```bash
python -m pip install pytest requests Faker python-dotenv pydantic email-validator
python -m pip freeze > requirements.txt
```

</details>

<details>
<summary><strong>Для чего каждая библиотека</strong></summary>

- `pytest`: запуск тестов, фикстуры, параметризация, маркеры.
- `requests`: HTTP-клиент.
- `Faker`: генерация данных (уникальные email/имена).
- `python-dotenv`: загрузка переменных из `.env`.
- `pydantic`: типизированные модели payload/response.
- `email-validator`: необходим для `EmailStr` в Pydantic.

</details>

<details>
<summary><strong>Как это связано с кодом</strong></summary>

- `tests/*` используют `pytest`.
- `clients/*` используют `requests`.
- `tests/conftest.py` использует `Faker`.
- `config.py` использует `python-dotenv`.
- `models/*` и `entities` используют `pydantic`.

</details>

---

## 3) Конфиг окружения (.env + config.py)

<details>
<summary><strong>Файл <code>.env</code></strong></summary>

```env
BASE_URL=https://stellarburgers.education-services.ru
```

</details>

<details>
<summary><strong>Файл <code>config.py</code></strong></summary>

```python
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "")
if not BASE_URL:
    raise ValueError("BASE_URL is not set")
```

</details>

<details>
<summary><strong>Зачем</strong></summary>

- Не хардкодим стенд в коде.
- Быстро переключаем окружения без правок Python-файлов.
- CI подставляет переменную централизованно.

</details>

---

## 4) Transport Layer (utils/requester.py)

<details>
<summary><strong>Идея</strong></summary>

Создаём `CustomRequester`: единая точка отправки HTTP-запросов, логирования и общих headers.

</details>

<details>
<summary><strong>Зачем</strong></summary>

- Не дублировать `requests.request(...)` по всему проекту.
- Единый формат логов для дебага.
- Клиенты становятся тонкими и чистыми.

</details>

<details>
<summary><strong>Связь с другими слоями</strong></summary>

- `clients/auth_client.py` использует `CustomRequester`.
- `tests` не работают с `requests` напрямую.

</details>

---

## 5) API Client Layer (clients/auth_client.py)

<details>
<summary><strong>Правило</strong></summary>

Один endpoint = один метод клиента.

Примеры:
- `register(...)`
- `login(...)`
- `get_user(...)`
- `patch_user(...)`
- `delete_user(...)`
- `refresh_token(...)`

</details>

<details>
<summary><strong>Зачем</strong></summary>

- Endpoint-логика не размазана по тестам.
- Проще менять URL/headers в одном месте.

</details>

---

## 6) Contracts и Entities (Pydantic)

<details>
<summary><strong>Какие документы создать</strong></summary>

- `models/base_model.py` -> общий `ApiModel`.
- `models/auth_models.py` -> response contracts.
- `models/auth_entities.py` -> payload + internal test entities.

</details>

<details>
<summary><strong>Пример <code>models/base_model.py</code></strong></summary>

```python
from pydantic import BaseModel, ConfigDict


def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class ApiModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
```

</details>

<details>
<summary><strong>Пример response contracts (<code>models/auth_models.py</code>)</strong></summary>

```python
from pydantic import EmailStr
from models.base_model import ApiModel


class UserModel(ApiModel):
    email: EmailStr
    name: str


class RegisterResponse(ApiModel):
    success: bool
    user: UserModel
    access_token: str
    refresh_token: str


class ErrorResponse(ApiModel):
    success: bool
    message: str
```

</details>

<details>
<summary><strong>Пример entities (<code>models/auth_entities.py</code>)</strong></summary>

```python
from pydantic import EmailStr
from models.base_model import ApiModel


class RegisterPayload(ApiModel):
    email: EmailStr
    password: str
    name: str


class RegisteredUser(ApiModel):
    access_token: str
    refresh_token: str
    email: EmailStr
    password: str
    name: str
```

</details>

<details>
<summary><strong>Как объяснять разницу на собесе</strong></summary>

- `auth_models`: контракт API-ответа (что пришло от сервера).
- `auth_entities`: данные, которыми управляет тест/воркфлоу внутри проекта.

</details>

---

## 7) Assertions Layer (assertions/*)

<details>
<summary><strong>Что делаем</strong></summary>

В assertions выносим парсинг и валидацию response.

Пример: `assert_user_registered(resp) -> RegisterResponse`.

</details>

<details>
<summary><strong>Зачем</strong></summary>

- Тесты становятся «бизнесовыми», а не JSON-парсерами.
- Повторное использование контрактных проверок.

</details>

---

## 8) Fixtures и test data (tests/conftest.py)

<details>
<summary><strong>Что делаем</strong></summary>

- Фикстура `auth_client`.
- Фикстура `user_credentials` (уникальный email).
- Фикстура `registered_user` с teardown удаления пользователя.

</details>

<details>
<summary><strong>Почему так</strong></summary>

- Управляем lifecycle тестовых данных.
- Минимизируем flaky из-за дублей пользователей.

</details>

---

## 9) Test Strategy: endpoint vs workflow

<details>
<summary><strong>Endpoint tests</strong></summary>

Проверяют конкретный endpoint изолированно.

Плюсы:
- быстрые;
- точная локализация поломки;
- хорошо идут в smoke.

</details>

<details>
<summary><strong>Workflow tests (services/auth_workflow.py)</strong></summary>

Проверяют бизнес-цепочки:
- register -> login;
- register -> update -> get;
- register -> logout -> refresh unauthorized.

Плюсы:
- проверка интеграции шагов;
- ближе к реальному пользовательскому сценарию.

</details>

---

## 10) Negative tests (важный принцип)

<details>
<summary><strong>Ключевая практика</strong></summary>

Для негативных кейсов (пустой email, пустой password и т.п.) не надо всегда использовать строгие Pydantic payload, иначе валидация упадет до запроса.

</details>

<details>
<summary><strong>Когда dict уместен</strong></summary>

- В негативных тестах, где нужно отправить заведомо невалидное тело на API и проверить ответ сервера.

</details>

---

## 11) Quality Gates: pre-commit + ruff + mypy

<details>
<summary><strong>Установка</strong></summary>

```bash
python -m pip install pre-commit ruff mypy types-requests
python -m pip freeze > requirements.txt
```

</details>

<details>
<summary><strong>Документ <code>.pre-commit-config.yaml</code> и его содержание</strong></summary>

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.5
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.19.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

</details>

<details>
<summary><strong>Как это работает</strong></summary>

- До коммита запускаются проверки качества.
- Если есть проблемы, коммит блокируется.
- Это твой локальный CI-гейт.

</details>

---

## 11.1) pyproject.toml (центральные настройки tools)

<details>
<summary><strong>Зачем нужен</strong></summary>

- Централизует настройки `ruff` и `mypy`.
- Не размазывает конфиг по CLI-командам.
- Упрощает перенос проекта в новый репозиторий.

</details>

<details>
<summary><strong>Документ <code>pyproject.toml</code> и пример содержания</strong></summary>

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = false
warn_return_any = true
warn_unused_configs = true
```

</details>

<details>
<summary><strong>Связь с CI и локальными командами</strong></summary>

- `pre-commit` читает правила линтера/типизации из `pyproject.toml`.
- CI использует те же правила, что и локальный запуск.

</details>

---

## 12) Pytest Markers (pytest.ini)

<details>
<summary><strong>Документ <code>pytest.ini</code> и содержание</strong></summary>

```ini
[pytest]
addopts = -v --alluredir=allure-results
markers =
    smoke: smoke API scenarios
    workflow: workflow API scenarios
    negative: negative API scenarios
    regression: regression API scenarios
```

</details>

<details>
<summary><strong>Как использовать</strong></summary>

```bash
pytest -m smoke -q
pytest -m workflow -q
pytest -m negative -q
pytest -m regression -q
```

</details>

---

## 13) Makefile (короткие команды команды)

<details>
<summary><strong>Документ <code>Makefile</code> и назначение</strong></summary>

Команды запуска в одном месте: `make lint`, `make test-smoke`, `make test`.

</details>

<details>
<summary><strong>Пример содержания</strong></summary>

```makefile
.PHONY: lint test test-smoke test-regression test-negative test-workflow

lint:
	.venv/bin/pre-commit run --all-files

test:
	.venv/bin/pytest -q

test-smoke:
	.venv/bin/pytest -m smoke -q

test-regression:
	.venv/bin/pytest -m regression -q

test-negative:
	.venv/bin/pytest -m negative -q

test-workflow:
	.venv/bin/pytest -m workflow -q
```

</details>

---

## 14) CI в GitHub Actions

<details>
<summary><strong>Документ <code>.github/workflows/ci.yml</code> и содержание</strong></summary>

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality-and-smoke:
    runs-on: ubuntu-latest
    env:
      BASE_URL: ${{ vars.BASE_URL }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run pre-commit
        run: pre-commit run --all-files

      - name: Run smoke tests
        run: pytest -m smoke -q --maxfail=1
```

</details>

<details>
<summary><strong>С чем связан этот документ</strong></summary>

- Использует `requirements.txt`.
- Использует `pytest.ini` (маркеры и addopts).
- Требует `BASE_URL` в `Settings -> Secrets and variables -> Actions -> Variables`.

</details>

---

## 15) Allure отчёты

<details>
<summary><strong>Установка</strong></summary>

```bash
python -m pip install allure-pytest
python -m pip freeze > requirements.txt
```

</details>

<details>
<summary><strong>Что добавить в CI</strong></summary>

```yaml
      - name: Upload Allure results artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: allure-results
          if-no-files-found: ignore
```

</details>

<details>
<summary><strong>Как смотреть</strong></summary>

1. Открыть run в GitHub Actions.
2. Скачать artifact `allure-results`.
3. Локально: `allure serve /path/to/allure-results`.

</details>

---

## 16) Git workflow и правила коммитов

<details>
<summary><strong>Ветка -> коммит -> push -> PR</strong></summary>

```bash
git checkout main
git pull
git checkout -b feat/some-change
# work
make lint
git add -A
git commit -m "feat(auth): add typed login response contract"
git push -u origin feat/some-change
```

</details>

<details>
<summary><strong>Конвенция коммитов</strong></summary>

- `feat(...)`: новая функциональность.
- `fix(...)`: багфикс.
- `test(...)`: изменения тестов.
- `chore(...)`: инфраструктура/инструменты.
- `docs(...)`: документация.

</details>

---

## 16.1) Branch Protection Rules (обязательно для командной разработки)

<details>
<summary><strong>Что включить в GitHub</strong></summary>

`Settings -> Branches -> Add classic branch protection rule`

- Branch name pattern: `main`
- `Require a pull request before merging`
- `Require approvals` (минимум 1)
- `Require status checks to pass before merging`
- Required status check: `quality-and-smoke`
- `Require branches to be up to date before merging` (рекомендуется)
- `Do not allow bypassing the above settings` (рекомендуется)

</details>

<details>
<summary><strong>Почему это важно</strong></summary>

- Никто не зальет ломающее изменение в `main`.
- CI становится реальным quality gate, а не «для галочки».
- Это стандарт реальных команд и собесов.

</details>

<details>
<summary><strong>Важный момент про required checks</strong></summary>

- Сначала должен хотя бы один раз отработать workflow (`CI`) на PR.
- Только после этого в выпадающем списке появится check `quality-and-smoke`.

</details>

---

## 17) Минимум для «готов к собесу»

<details>
<summary><strong>Checklist</strong></summary>

- Есть слой clients/assertions/models/services/tests.
- Есть негативные и workflow тесты.
- Есть pre-commit + ruff + mypy.
- Есть маркеры smoke/workflow/negative/regression.
- Есть CI, который гоняет quality + smoke.
- Есть Allure artifact в CI.
- Есть понятный README с командами запуска.

</details>

---

## 18) Частые ошибки (и как не делать)

<details>
<summary><strong>Топ-ошибки джуна</strong></summary>

- Пуш прямо в `main`.
- Тесты сами парсят JSON, assertions пустые.
- Негативные кейсы валятся в Pydantic до запроса.
- Нет teardown, тесты конфликтуют между собой.
- Нет marker strategy, всё гоняется всегда.
- Нет CI-гейта, качество не контролируется.

</details>

---

## 19) Что делать в каждом новом проекте (короткая схема)

<details>
<summary><strong>Порядок внедрения</strong></summary>

1. Каркас + env конфиг.
2. Клиент + transport.
3. Контракты + assertions.
4. Endpoint happy path + negative.
5. Workflow слой.
6. Маркеры.
7. Pre-commit quality gates.
8. CI.
9. Allure artifacts.
10. README + branch protection.

</details>

---

## 20) Best Practices (добавить сразу в новый проект)

<details>
<summary><strong>Технические практики</strong></summary>

- Таймауты на каждый HTTP-запрос (никогда не оставлять бесконечный wait).
- Уникальные тестовые данные (`uuid` в email/логине).
- Явные teardown-шаги (удаление созданных сущностей).
- Логи запроса/ответа без утечки секретов.
- Разделение позитивных/негативных сценариев по маркерам.

</details>

<details>
<summary><strong>Практики по архитектуре тестов</strong></summary>

- Endpoint-тесты держать быстрыми и точечными.
- Workflow-тесты покрывают только ключевые бизнес-цепочки.
- Assertions возвращают typed model, а не сырой dict.
- Fixtures делают setup/teardown, не бизнес-проверки.

</details>

<details>
<summary><strong>Практики по процессу</strong></summary>

- Каждый change через ветку и PR.
- Перед коммитом: `make lint`.
- Перед PR: `make test-smoke` и нужный таргет (`workflow/negative`).
- После merge: удалить feature-ветку локально и remote.

</details>

---

## 21) Шаблон переноса в другой проект (Copy/Paste Checklist)

<details>
<summary><strong>Быстрый чеклист</strong></summary>

1. Создать каркас папок и базовые файлы.
2. Поднять `.venv`, установить зависимости, заморозить `requirements.txt`.
3. Настроить `.env` + `config.py`.
4. Добавить transport (`CustomRequester`) и API clients.
5. Добавить contracts/entities и слой assertions.
6. Добавить фикстуры и первые smoke endpoint-тесты.
7. Добавить workflow слой.
8. Настроить `pre-commit`, `pyproject.toml`, `Makefile`.
9. Добавить GitHub Actions CI.
10. Добавить Allure artifact upload.
11. Включить Branch Protection для `main`.
12. Обновить README командами запуска.

</details>
