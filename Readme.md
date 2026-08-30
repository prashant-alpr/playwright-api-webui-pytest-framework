# Playwright API Web UI Pytest Automation Framework

[![Order Booking UI API Tests](https://github.com/prashant-alpr/playwright-api-webui-pytest-framework/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/prashant-alpr/playwright-api-webui-pytest-framework/actions/workflows/e2e-tests.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12.0-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-v1.62.0-green.svg)
![Pytest](https://img.shields.io/badge/pytest-v9.1.1-orange.svg)

An enterprise-grade API Web UI automation framework built with **Python, Pytest, and Playwright**, demonstrating advanced api, web automation patterns against a highly dynamic order booking platform (https://rahulshettyacademy.com/client/#/dashboard/dash). 

## 🏗️ Architecture & Technical Highlights

This project is structured using a strict **Page Object Model (POM)** and showcases solutions to common complex automation challenges:

* **Session State Management:** Login is performed through API and the Session state is sent to the browser context which loads the Home page directly.
* **Page Object Model (POM):** Clean separation of page locators, interactions, and test logic for high maintainability.
* **Service Object Pattern:** Decouples API endpoint definitions and payload structures from test assertion logic for scalable test design.
* **Automated Request/Response Logging:** Captures full HTTP details (HTTP method, target URL, query params, request body, status codes, and JSON response payloads) directly into timestamped `pytest-html` reports.
* **Session-Scoped Fixture Authentication:** Pre-authenticates test runs via session-scoped Pytest fixtures to eliminate redundant login requests and speed up execution.
* **Dynamic Context Management:** Implements Playwright's `expect_page()` context managers to seamlessly intercept, capture, and switch execution states.
* **Resilient Synchronization:** Avoids hard-coded sleeps (`time.sleep`) entirely. Utilizes Playwright's auto-waiting mechanisms and DOM state evaluations (e.g., waiting for dynamic cart counters to update via injected JavaScript evaluation) for flaky-free execution.
* **Modular Configuration:** Browser initialization and teardown are decoupled using Pytest `conftest.py` fixtures with distinct session and function scopes.
* **Automated CI/CD:** Integrated GitHub Actions workflow running on pushes, pull requests, and scheduled nightly builds with HTML artifact deployment.

## 🛠️ Tech Stack

* **Language:** Python 3.12.0+
* **Core Tool:** Playwright for Python
* **Test Runner:** `pytest`
* **Reporting:** `pytest-html`
* **CI/CD:** GitHub Actions


## 📂 Project Structure

```text
order_booking /
├── conftest.py                 # Core Playwright browser & context fixtures
├── api_endpoints /
│   └── api_endpoints.py        # API service layer endpoints
├── config /
│   └── config.py               # Base URL details
├── data /
│   ├── api_data.py             # API payload data
│   ├── home_page_data.py       # Home page data
│   └── order_page_data.py      # Order page data
├── locators /
│   ├── home_page_locators.py   # Home Page locators
│   └── order_page_locators.py  # Order page locators
├── pages/
│   ├── home_page.py            # Utilities and reusable methods of Home page
│   └── order_page.py           # Reusable methods of Order page
├── tests/
│   └── test_order_booking.py   # E2E test execution flow
├── results                     # Test Results html report
├── requirements.txt            # Library details
├── pytest.ini                  # Pytest execution command, markers and logging config
├── .github/workflows
│   └── e2e-tests.yml           # CI/CD Github Actions pipeline implementation                  
└── README.md
