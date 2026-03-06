# Stellar Burgers API Autotests

## Project Overview
API autotest framework for auth-related scenarios of Stellar Burgers service.
The project demonstrates layered test architecture, typed contracts, reusable workflows, and CI quality gates.

## Stack
- Python 3.11
- pytest
- requests
- pydantic
- Faker
- python-dotenv
- ruff + mypy + pre-commit
- GitHub Actions

## Architecture
- `clients/` - endpoint-level API clients (`AuthClient`)
- `utils/` - transport layer (`CustomRequester`) and request/response logging
- `models/` - typed models:
  - `auth_models.py` - API response contracts
  - `auth_entities.py` - internal test entities/payloads
- `assertions/` - contract/business assertions over API responses
- `services/` - multi-step workflows (`AuthWorkflow`)
- `tests/` - endpoint and workflow tests
- `tests/conftest.py` - fixtures and dependency wiring

## Test Markers Strategy
- `smoke` - critical fast checks for core functionality
- `workflow` - multi-step scenario tests
- `negative` - invalid/unauthorized behavior checks
- `regression` - broader stable suite (happy + negative coverage)

## Configuration
Environment variable:
- `BASE_URL` (example: `https://stellarburgers.education-services.ru`)

You can set it via `.env`:

```env
BASE_URL=https://stellarburgers.education-services.ru
```

## Local Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Quality Checks

```bash
.venv/bin/pre-commit run --all-files
```

## Test Runs

```bash
.venv/bin/pytest -q
.venv/bin/pytest -m smoke -q
.venv/bin/pytest -m workflow -q
.venv/bin/pytest -m negative -q
.venv/bin/pytest -m regression -q
```

## CI
GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- dependency installation
- `pre-commit run --all-files`
- smoke tests (`pytest -m smoke -q --maxfail=1`)

Repository variable required for CI:
- `BASE_URL`

## Current Coverage
Implemented:
- auth happy-path endpoints
- auth negative scenarios
- workflow scenarios:
  - register + login
  - register + update + get
  - register + logout + get
  - register + logout + refresh unauthorized

## Roadmap
- expand coverage beyond auth domain
- add richer reporting (for example, Allure)
- improve flaky-test strategy and retries where needed
- add more boundary/contract edge cases
