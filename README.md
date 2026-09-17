# ParaBank Playwright + Pytest Test Automation Framework

A Python test automation framework built with **Playwright** and **pytest** that exercises the core customer-facing workflows of the [ParaBank](https://parabank.parasoft.com/parabank/index.htm) demo banking application: account registration, login, and loan requests.

## Overview

This framework automates end-to-end browser testing of ParaBank, a publicly available demo banking site maintained by Parasoft for testing tool evaluation. It is built to demonstrate a clean, maintainable automation architecture rather than to provide exhaustive coverage of the application.

- **Application under test:** ParaBank demo site (`https://parabank.parasoft.com/parabank/index.htm`)
- **Automation technology:** Playwright's synchronous Python API, driven through the `pytest-playwright` plugin
- **Testing approach:** UI-driven, black-box end-to-end tests that interact with the application exactly as a user would — filling forms, clicking buttons, and asserting on visible page state
- **Structure rationale:** The project follows the **Page Object Model (POM)**, separating page interaction logic (`pages/`) from test logic (`tests/`), with reusable random test data (`utils/`) and static test data (`test_data/`) kept independent of both. This keeps individual tests short and readable while centralising selector maintenance in one place per page.

## Technology Stack

Based on `requirements.txt`:

| Package | Version | Purpose |
|---|---|---|
| `pytest` | 9.1.1 | Test runner and framework |
| `pytest-playwright` | 0.9.0 | Integrates Playwright with pytest (browser/page fixtures, CLI options) |
| `playwright` | 1.56.0 | Browser automation engine |
| `pytest-html` | 4.2.0 | Generates the self-contained HTML test report |
| `pytest-metadata` | 3.1.1 | Supplies environment metadata to the HTML report |
| `pytest-base-url` | 2.1.0 | Provides the `base_url` fixture and `--base-url` / `PYTEST_BASE_URL` support |
| `python-slugify` | 8.0.4 | Used in `conftest.py` to build artifact folder names matching Playwright's own naming |

## Features

Implemented framework capabilities, verified against the codebase:

- **Page Object Model** — one class per application page/flow (`pages/login_page.py`, `pages/register_page.py`, `pages/request_loan.py`)
- **Browser automation via Playwright**, driven through `pytest-playwright`'s built-in `page` fixture
- **Chromium execution**, fixed as the default browser via `--browser chromium` in `pytest.ini`
- **Dynamic test data** — random usernames, passwords, loan amounts and down payments generated per test run (`utils/random_data.py`)
- **Screenshots on failure**, with full-page capture enabled (`--screenshot=only-on-failure --full-page-screenshot`)
- **Playwright tracing on failure** (`--tracing=retain-on-failure`)
- **Video recording** — not enabled by default locally; enabled explicitly in CI (`--video=retain-on-failure`)
- **Self-contained HTML reporting** (`pytest-html`), with failure screenshots and other artifacts embedded as report "extras" via a custom `conftest.py` hook
- **JUnit XML reporting** (`--junitxml=reports/junit.xml`)
- **Pytest markers** — `smoke` and `regression` are registered under `--strict-markers` for future use (see [Test Coverage](#test-coverage) — no test currently applies either marker)
- **CI/CD execution** via GitHub Actions on every push/PR to `main`, plus manual dispatch
- **Playwright browser caching** in CI, keyed by resolved Playwright version
- **Failure evidence collection** — screenshots, traces and (in CI) videos are uploaded as workflow artifacts

## Project Structure

```text
playwright-pytest-framework/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml   # CI pipeline definition
├── pages/
│   ├── login_page.py              # Login/logout page object
│   ├── register_page.py           # Registration page object
│   └── request_loan.py            # Loan request page object
├── tests/
│   ├── test_login.py              # Login test(s)
│   ├── test_register.py           # Registration test(s)
│   └── test_request_loan.py       # Loan request test(s)
├── test_data/
│   └── personal_details.py        # Static default personal details used on registration
├── utils/
│   └── random_data.py             # Random username/password/loan data generators
├── reports/                        # Generated: HTML + JUnit reports (git-ignored)
├── test-results/                   # Generated: Playwright screenshots/traces/videos (git-ignored)
├── conftest.py                    # Shared fixtures and report-artifact wiring
├── pytest.ini                     # Central pytest/Playwright configuration
├── requirements.txt                # Pinned Python dependencies
└── README.md
```

- **`pages/`** — one Page Object per screen/flow, encapsulating locators and interactions.
- **`tests/`** — test cases only; they call into page objects and assert on outcomes.
- **`test_data/`** — static, non-random data (e.g. the default registration details).
- **`utils/`** — pure helper functions, currently focused on generating randomised test data.
- **`conftest.py`** — the `registered_user` fixture and the logic that attaches failure artifacts to the HTML report.
- **`reports/`** and **`test-results/`** are generated at test-run time and are excluded from version control via `.gitignore`.

## Test Architecture

The framework is organised into four co-operating layers:

1. **Tests (`tests/`)** — express *what* is being verified. They read as a sequence of user actions and expected outcomes, delegating all element interaction to page objects.
2. **Page Objects (`pages/`)** — express *how* to interact with a given page. Each class exposes locators as attributes and interactions (e.g. `login()`, `register()`, `apply_for_loan()`) as methods. Page objects also expose `expect_*` assertion helper methods (e.g. `expect_registration_success()`, `expect_loan_approved()`), keeping Playwright's `expect()` assertions colocated with the locators they check.
3. **Fixtures (`conftest.py`)** — supply shared setup, most notably `registered_user`, which registers a fresh random user and returns their credentials so dependent tests start from a known, isolated state.
4. **Configuration and reporting (`pytest.ini`, `conftest.py`)** — `pytest.ini` centralises all Playwright/pytest CLI options so they apply automatically on every run; `conftest.py` post-processes each test's artifact folder after teardown and embeds screenshots/traces into the HTML report as "extras".

Playwright itself is only ever accessed through `pytest-playwright`'s fixtures (`page`, `base_url`) — there are no custom browser or browser-context fixtures in this project.

## Prerequisites

- **Python 3.12** (the version used in CI; `pytest.ini` requires pytest `>= 8.0`, and the pinned `pytest==9.1.1` requires a reasonably current Python 3)
- **Git**, to clone the repository
- **Playwright's Chromium browser**, installed via the `playwright install` command (see below) — no other browsers are required, since the suite is pinned to Chromium
- Internet access to reach `https://parabank.parasoft.com`, since there is no local/mocked instance of the application

## Installation

**Windows (PowerShell):**

```powershell
git clone <repository-url>
cd playwright-pytest-framework

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python -m playwright install chromium
```

**macOS/Linux:**

```bash
git clone <repository-url>
cd playwright-pytest-framework

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m playwright install chromium
```

> Only the Chromium browser is installed above since it is the only browser the suite runs against (`--browser chromium` in `pytest.ini`). Omit `chromium` from the install command if you want all Playwright browsers available locally.

## Running the Tests

All commands below assume the virtual environment is activated and are run from the project root, where `pytest.ini` lives.

```bash
# Run the full suite (uses every setting from pytest.ini automatically)
pytest

# Run a specific test file
pytest tests/test_login.py

# Run a specific test
pytest tests/test_request_loan.py::TestRequestLoan::test_loan_request_approved_with_valid_data

# Run tests headed (visible browser window) instead of the Playwright default
pytest --headed

# Override the base URL for a single run
pytest --base-url https://parabank.parasoft.com/parabank/index.htm

# Useful debugging options
pytest -v                 # verbose test names
pytest --headed --slowmo 500   # slow down interactions for visual debugging
pytest -k "register"      # run only tests whose name matches "register"
```

`smoke` and `regression` markers are registered in `pytest.ini` (so `pytest -m smoke` or `pytest -m regression` will run without error), but no current test is tagged with either — see [Future Improvements](#future-improvements).

## Pytest Configuration

All settings live in `pytest.ini` and apply automatically to every `pytest` invocation — no extra flags are required for a standard run:

| Setting | Value | Effect |
|---|---|---|
| `testpaths` | `tests` | Test discovery is limited to the `tests/` directory |
| `pythonpath` | `.` | Project root is added to `sys.path`, so `pages`, `utils` and `test_data` import cleanly |
| `base_url` | `https://parabank.parasoft.com/parabank/index.htm` | Default target for the `base_url` fixture (from `pytest-base-url`) |
| `--browser chromium` | — | Fixes the browser under test to Chromium |
| `--output=test-results` | — | Directory Playwright artifacts (screenshots, traces) are written to |
| `--screenshot=only-on-failure` | — | Screenshot captured only when a test fails |
| `--full-page-screenshot` | — | Failure screenshots capture the entire scrollable page, not just the viewport |
| `--tracing=retain-on-failure` | — | Playwright trace is kept only for failed tests |
| `--html=reports/test-report.html` / `--self-contained-html` | — | Single-file HTML report with all assets inlined |
| `--junitxml=reports/junit.xml` | — | JUnit XML report for CI integration |
| `markers` | `smoke`, `regression` | Registers the two custom markers, enforced by `--strict-markers` |
| `--strict-markers` / `--strict-config` | — | Fails fast on unknown markers or invalid ini options, catching typos early |
| `-ra` | — | Prints a short summary of all non-passing results at the end of the run |
| `--durations=10` | — | Reports the 10 slowest tests |
| `log_cli` / `log_level` / `log_format` / `log_date_format` | `false` / `INFO` / custom | Logging is captured (not streamed live) at `INFO` level, with a timestamped format |
| `filterwarnings` | `default` | Uses Python's default warning behaviour rather than suppressing or escalating warnings |

Video recording (`--video=retain-on-failure`) is **not** part of `pytest.ini` and is therefore off by default locally; it is passed explicitly as a CLI flag in the CI workflow.

## Test Data

- **Static data** lives in `test_data/personal_details.py` as `DEFAULT_PERSONAL_DETAILS` — a fixed set of registration fields (name, address, phone, SSN) reused across registration-related tests, since these fields don't need to vary for the scenarios currently covered.
- **Dynamic data** is generated by `utils/random_data.py` for anything that must be unique per test run:
  - `random_username()` — an 8-character random alphanumeric suffix appended to a prefix, avoiding username collisions between runs.
  - `random_password()` — builds a 16-character password by drawing from letters, digits and punctuation using Python's `secrets` module (rather than `random`), so each generated password is cryptographically randomised and each test registers and authenticates as a genuinely fresh user rather than depending on a shared, static account.
  - `random_loan_amount()` / `random_down_payment()` — randomised loan and down-payment figures for the loan-request tests, with the down payment capped at 90% of the loan amount to stay within valid input ranges.
  - `expected_loan_date()` — formats today's date to match the format ParaBank displays for an approved loan.

This approach means the test suite doesn't depend on any pre-seeded user in the ParaBank database — every test that needs an authenticated user registers one for itself.

## Page Object Model

Each page object represents one screen or flow of the application and follows the same shape:

- **Locators** are defined as instance attributes in `__init__`, using Playwright's role-based and CSS locators (e.g. `page.get_by_role("button", name="Log In")`, `page.locator("#customer\\.firstName")`).
- **Interactions** (clicking, filling fields) are plain methods on the class, e.g. `LoginPage.login()`, `RegisterPage.fill_personal_details()`, `RequestLoanPage.apply_for_loan()`.
- **Assertions** live in dedicated `expect_*` methods on the same class (e.g. `RegisterPage.expect_registration_success()`, `RequestLoanPage.expect_loan_approved()`), so a test simply calls `page_object.expect_x()` rather than importing Playwright's `expect` directly.
- Tests instantiate the relevant page object(s) and call these interaction/assertion methods — they never touch a raw locator directly.

**Existing page objects:**

| Page Object | Represents | Key methods |
|---|---|---|
| `LoginPage` | Login form and logout link | `goto()`, `login()`, `log_out()` |
| `RegisterPage` | Customer registration form | `go_to_register()`, `fill_personal_details()`, `fill_credentials()`, `register()`, `expect_registration_success()`, `expect_first_name_required_error()` |
| `RequestLoanPage` | Loan request flow, including the resulting new-account view | `go_to_request_loan()`, `fill_amount()`, `fill_down_payment()`, `apply_for_loan()`, `expect_error()`, `expect_loan_processed()`, `expect_loan_approved()`, `expect_account_details()` |

## Fixtures

Defined in `conftest.py`:

| Fixture | Scope | Purpose |
|---|---|---|
| `registered_user` | function (default) | Registers a brand-new user with a random username/password (via `random_username()`/`random_password()`) and the shared `DEFAULT_PERSONAL_DETAILS`, asserts the registration succeeded, and returns a dict containing the `page`, `username` and `password`. Used by tests that need an already-authenticated session (login, loan request tests) so each test starts from a clean, isolated account. |

The `page` and `base_url` fixtures used throughout the suite come from `pytest-playwright` and `pytest-base-url` respectively and are not redefined in this project.

## Test Reporting

- **HTML report** — generated at `reports/test-report.html` as a single, self-contained file (all CSS/assets inlined via `--self-contained-html`), so it can be opened directly in a browser or shared as one file.
- **JUnit XML report** — generated at `reports/junit.xml`, suitable for consumption by CI systems or dashboards.
- **Screenshots** — captured only on failure, as full-page images, into `test-results/<test-slug>/`.
- **Traces** — retained only on failure, into `test-results/<test-slug>/trace.zip`.
- **Videos** — not recorded locally by default; recorded on failure only when `--video=retain-on-failure` is passed (as it is in CI).
- **Artifact–report association** — a `pytest_runtest_makereport` hook in `conftest.py` runs after each test's teardown, locates that test's artifact directory (named to match Playwright's own slugified node ID), and attaches every file it finds to the HTML report: images are embedded inline as base64, while other files (traces, videos) are linked by path as report "extras". This is what makes screenshots visible directly inside `test-report.html` without opening `test-results/` separately.

## Failure Investigation

When a test fails, a practical order to investigate is:

1. Open `reports/test-report.html` in a browser.
2. Find the failed test and expand it to see the assertion error and any embedded screenshot.
3. If a screenshot isn't conclusive, locate the matching folder under `test-results/` and open `trace.zip` with `playwright show-trace test-results/<test-slug>/trace.zip` to step through the full run (DOM snapshots, network, console).
4. Check for a video in the same folder if the run included `--video=retain-on-failure`.
5. Re-run the single failing test locally, optionally headed, to reproduce interactively:
   ```bash
   pytest tests/test_request_loan.py::TestRequestLoan::test_loan_request_approved_with_valid_data --headed
   ```

## CI/CD

Defined in `.github/workflows/playwright-tests.yml`:

- **Triggers:** every push to `main`, every pull request targeting `main`, and manual runs via `workflow_dispatch`.
- **Concurrency:** runs in the same workflow/ref group are cancelled in favour of the latest one (`cancel-in-progress: true`), avoiding redundant parallel runs.
- **Environment:** `ubuntu-latest`, Python **3.12**, with pip caching keyed on `requirements.txt`.
- **Dependency installation:** `pip install -r requirements.txt`.
- **Playwright browser installation:** the installed `playwright` package version is resolved at runtime, the Playwright Chromium browser cache is restored/saved keyed on that version (`~/.cache/ms-playwright`), and `playwright install --with-deps chromium` installs the browser plus required OS-level dependencies.
- **Test execution:** `python -m pytest --video=retain-on-failure` — this is the **only** CLI flag added in CI; every other setting (browser, base URL, screenshots, tracing, reporting paths, markers) comes from `pytest.ini`, so CI and local runs stay in sync by construction.
- **Reports and artifacts:** on every run (`if: always()`), the `reports/` directory (HTML + JUnit) is uploaded as `test-reports-<run-number>`, retained 30 days; `test-results/` (screenshots, traces, videos) is uploaded as `failure-evidence-<run-number>`, retained 14 days.
- **Run summary:** a short Markdown summary (base URL and artifact names) is written to the GitHub Actions job summary at the end of the run.

## Reports and Artifacts

| Location | Purpose |
|---|---|
| `reports/test-report.html` | Self-contained HTML test report with embedded failure screenshots |
| `reports/junit.xml` | JUnit XML report for CI/tooling consumption |
| `test-results/` | Per-test folders containing Playwright screenshots and trace files (and videos, when enabled) |

Both `reports/` and `test-results/` are regenerated on every run and are excluded from version control via `.gitignore`.

## Test Coverage

Currently implemented scenarios, grouped by feature area (7 test cases across 3 files):

**Login** (`tests/test_login.py`)
- Logging out of a freshly registered account and logging back in with the same credentials succeeds and lands on the Accounts Overview page.

**Registration** (`tests/test_register.py`)
- Registering a new customer with a complete, valid set of details succeeds.
- Submitting the registration form with a missing first name shows the expected required-field error.

**Loan Request** (`tests/test_request_loan.py`)
- Submitting a loan request with no amount entered shows an error.
- Submitting a loan request with an amount but no down payment shows an error.
- Submitting a loan request with valid, randomised amount and down-payment data results in an approved loan, showing the expected provider and date.
- After a successful loan request, the newly created loan account's details page displays correctly.

This is a targeted, scenario-based suite rather than exhaustive coverage of ParaBank's full feature set (transfers, bill pay, account activity, etc. are not currently automated).

## Coding and Framework Practices

Practices actually demonstrated by this project:

- Page Object Model separating locators/interactions from test logic
- A reusable fixture (`registered_user`) for shared setup
- Dynamic, randomly generated test data instead of shared static accounts
- Explicit `expect_*` assertion helpers colocated with their page objects
- Centralised configuration in `pytest.ini`, applied automatically to every run
- Automatic failure-evidence collection (screenshots, traces) wired into the HTML report
- CI integration that reuses the same `pytest.ini` configuration rather than duplicating it
- Dependency pinning in `requirements.txt`, with exact versions verified against a committed test run
- Clear separation of static test data (`test_data/`) from random test-data generation (`utils/`) and from test logic (`tests/`)

## Troubleshooting

- **Virtual environment not activating (Windows):** if PowerShell blocks the activation script, run PowerShell as Administrator once and execute `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry `.venv\Scripts\Activate.ps1`.
- **`ModuleNotFoundError` for `pages`, `utils` or `test_data`:** ensure you're running `pytest` from the project root; `pythonpath = .` in `pytest.ini` depends on this.
- **Playwright browsers not installed:** if you see an error about a missing browser executable, run `python -m playwright install chromium`.
- **Tests can't reach ParaBank / timeouts on `page.goto`:** confirm you have internet access and that `https://parabank.parasoft.com` is reachable from your network; the suite has no offline/mocked mode.
- **`reports/` or `test-results/` not created:** these are only created on first test run in the project root — confirm you're running `pytest` (not `python -m unittest` or similar) from the correct directory and that `pytest.ini` is being picked up (check the `pytest_report_header` output at the top of the run).
- **CI failures that don't reproduce locally:** compare the Python version (CI uses 3.12) and confirm `requirements.txt` versions match what's installed locally (`pip freeze`); also check whether the CI run's `failure-evidence-*` artifact shows a transient site issue (e.g. a bot-protection challenge page) rather than a framework/application defect.
- **Missing artifacts in the HTML report:** artifacts are only attached for tests whose artifact folder actually exists after teardown; if `--output` was overridden on the command line, the report hook in `conftest.py` looks in that same overridden location.

## Future Improvements

The following are reasonable extensions to this framework but are **not currently implemented**:

- Applying the existing `smoke` and `regression` markers to tests so subsets can be run selectively
- Additional browser coverage (Firefox, WebKit) beyond the current Chromium-only configuration
- API-level testing to complement the current UI-only approach
- Parallel test execution (e.g. via `pytest-xdist`)
- Expanded coverage of other ParaBank features (transfers, bill pay, account activity, find transactions)
- Additional CI quality gates (e.g. linting, type checking) ahead of the test run
