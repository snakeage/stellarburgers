# Interview Notes (Stellar Burgers AQA Project)

## 1) Why layered architecture?
I separated `clients`, `assertions`, `models`, `entities`, `services`, and `tests` to reduce coupling and improve maintainability.
Each layer has a single responsibility, so changes are localized and easier to debug.

## 2) What does each layer do?
- `clients`: endpoint-level API calls.
- `assertions`: response/business validations.
- `models`: API response contracts (Pydantic).
- `entities`: internal payload/state objects for tests.
- `services`: multi-step workflows.
- `tests`: readable scenario specs.

## 3) Why both endpoint tests and workflow tests?
Endpoint tests localize defects in a specific API method.
Workflow tests validate multi-step business flows and integration of steps.
They cover different risk types and should coexist.

## 4) Why use Pydantic for response validation?
To replace manual JSON key checks with typed contract validation.
It reduces noise, improves consistency, and catches schema/type drift early.

## 5) Why entities if response models already exist?
Response models represent API output.
Entities represent internal test state and payloads needed across steps (for example `RegisteredUser`).

## 6) Why pre-commit if CI exists?
Shift-left quality checks:
- faster local feedback
- less CI noise
- cleaner commits
I run `ruff`, `ruff-format`, and `mypy` before commit.

## 7) How did you reduce flaky behavior?
- unique email generation with UUID to avoid collisions
- marker-based run strategy (`smoke/workflow/regression/negative`)
- env-based config (`BASE_URL`)
- CI quality gate for smoke and static checks

## 8) Marker strategy in your project
- `smoke`: critical fast checks
- `workflow`: multi-step scenarios
- `negative`: invalid/unauthorized behavior
- `regression`: broad stable set (happy + negative)

## 9) What CI is configured?
GitHub Actions pipeline:
- install dependencies
- run pre-commit
- run smoke tests
- upload `allure-results` artifact

## 10) How do you use Allure in CI?
I download `allure-results` artifact from workflow run and open report locally via:
`allure serve <path>`.

## 11) What was a key debugging lesson?
Do not assume logout invalidates access token.
I verified real API behavior and adjusted workflow expectations accordingly.

## 12) How do you work with branches?
Feature branch -> commit -> push -> PR -> CI -> merge.
Main branch is protected by checks/PR flow.
