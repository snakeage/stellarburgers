# AQA API Playbook (Short / Daily)

> Версия для ежедневной работы: минимум текста, максимум действий.

## 1. Создать каркас

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
Makefile
.github/workflows/ci.yml
requirements.txt
.gitignore
README.md
```

## 2. Поднять окружение

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 3. Установить базовые библиотеки

```bash
python -m pip install pytest requests Faker python-dotenv pydantic email-validator
python -m pip freeze > requirements.txt
```

## 4. Конфиг окружения

`.env`
```env
BASE_URL=https://your-api-url
```

`config.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "")
if not BASE_URL:
    raise ValueError("BASE_URL is not set")
```

## 5. Правило слоёв

- `clients` -> endpoint вызовы
- `assertions` -> проверки контрактов
- `models` -> response contracts
- `entities` (в `auth_entities.py`) -> payload + данные для тестов
- `services` -> workflow цепочки
- `tests` -> сценарии

## 6. Маркеры тестов

`pytest.ini`
```ini
[pytest]
addopts = -v --alluredir=allure-results
markers =
    smoke: smoke API scenarios
    workflow: workflow API scenarios
    negative: negative API scenarios
    regression: regression API scenarios
```

Запуск:
```bash
pytest -m smoke -q
pytest -m workflow -q
pytest -m negative -q
pytest -m regression -q
```

## 7. Quality Gates

Установка:
```bash
python -m pip install pre-commit ruff mypy types-requests
python -m pip freeze > requirements.txt
```

`.pre-commit-config.yaml`
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

`pyproject.toml`
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

Проверка:
```bash
make lint
```

## 8. Makefile

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

## 9. CI (GitHub Actions)

`.github/workflows/ci.yml`
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
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: pre-commit run --all-files
      - run: pytest -m smoke -q --maxfail=1
      - name: Upload Allure results artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: allure-results
          if-no-files-found: ignore
```

GitHub settings:
- `Settings -> Secrets and variables -> Actions -> Variables`
- создать `BASE_URL`

## 10. Allure

```bash
python -m pip install allure-pytest
python -m pip freeze > requirements.txt
```

`.gitignore`
```gitignore
allure-results/
```

Просмотр из CI:
1. Actions -> run -> artifact `allure-results`
2. скачать
3. `allure serve /path/to/allure-results`

## 11. Git workflow

```bash
git checkout main
git pull
git checkout -b feat/your-change
# changes
make lint
git add -A
git commit -m "feat(scope): short description"
git push -u origin feat/your-change
```

## 12. Branch protection

`Settings -> Branches -> Add classic branch protection rule`:
- pattern: `main`
- Require PR before merging
- Require approvals (1)
- Require status checks to pass
- required check: `quality-and-smoke`
- Require branches to be up to date (recommended)

## 13. Быстрый чеклист перед PR

- `make lint` зелёный
- `make test-smoke` зелёный
- нужные `workflow/negative` прогнаны
- README обновлён при изменении процесса
- нет мусора в git (`git status` clean)
