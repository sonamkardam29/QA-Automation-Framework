# 🧪 QA Automation Testing Framework

A modular, production-ready **UI Test Automation Framework** built with **Python**, **Selenium WebDriver**, **Pytest**, and **GitHub Actions**. Designed for automated regression testing of the demo e-commerce website [SauceDemo](https://www.saucedemo.com/).

This project demonstrates professional SDET (Software Development Engineer in Test) design patterns, including the **Page Object Model (POM)**, reusable fixtures, clean assertions, automatic failure screenshot capturing, self-contained HTML reporting, and Continuous Integration (CI).

---

## 📋 Table of Contents
- [🎯 Objectives](#-objectives)
- [⚙️ Tech Stack](#️-tech-stack)
- [🏗️ Project Architecture & POM](#️-project-architecture--pom)
- [📁 Folder Structure](#-folder-structure)
- [🧪 Test Scenarios](#-test-scenarios)
- [🚀 Quick Start & Installation](#-quick-start--installation)
- [📊 Execution & Reports](#-execution--reports)
- [🤖 GitHub Actions CI/CD](#-github-actions-cicd)
- [🔮 Future Improvements](#-future-improvements)

---

## 🎯 Objectives

1. **Maintainability**: Decouple page element locators and page operations from test execution logic using Page Object Model.
2. **Robustness**: Utilize Selenium explicit waits (`WebDriverWait` and `expected_conditions`) to prevent flaky tests.
3. **Traceability**: Automatically capture screenshots on test failures and embed them directly into self-contained HTML execution reports.
4. **Automation in CI**: Execute headless automated test runs on every GitHub `push` and `pull_request` event.

---

## ⚙️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **Automation Tool** | Selenium WebDriver 4 | Web browser automation engine |
| **Test Runner** | Pytest | Test discovery, parametrization, and assertion runner |
| **Reporting** | Pytest-HTML | Self-contained HTML test report generator |
| **Design Pattern** | Page Object Model (POM) | Architectural design for maintainable UI automation |
| **CI/CD** | GitHub Actions | Automated workflow for headless Linux test runs |

---

## 🏗️ Project Architecture & POM

The framework separates the codebase into 3 core layers:
1. **Pages Layer (`pages/`)**: Contains web page objects with private/protected locators and page interaction methods.
2. **Tests Layer (`tests/`)**: Contains test functions that invoke Page Object methods and validate behaviors using Pytest assertions.
3. **Utils & Config (`utils/` & `conftest.py`)**: Manages browser setup, environment constants, fixture teardowns, and reporting hooks.

```
+-------------------------------------------------------------+
|                        Test Layer                           |
|  (test_login.py, test_cart.py, test_sorting.py)             |
+------------------------------+------------------------------+
                               | calls page methods
                               v
+-------------------------------------------------------------+
|                      Page Object Layer                      |
|  (LoginPage, InventoryPage, CartPage)                        |
+------------------------------+------------------------------+
                               | interacts via Selenium
                               v
+-------------------------------------------------------------+
|                      Target Web Application                 |
|                   (https://www.saucedemo.com/)              |
+-------------------------------------------------------------+
```

---

## 📁 Folder Structure

```
qa-automation-framework/
│
├── pages/                  # Page Object Model classes
│   ├── __init__.py
│   ├── login_page.py       # LoginPage locators & interactions
│   ├── inventory_page.py   # Inventory catalog interactions & sorting
│   └── cart_page.py        # Shopping cart interactions
│
├── tests/                  # Automated Pytest test suites
│   ├── __init__.py
│   ├── test_login.py       # Login positive & negative tests
│   ├── test_cart.py        # Cart addition and removal tests
│   └── test_sorting.py     # Product catalog sorting tests
│
├── utils/                  # Project configuration and helpers
│   ├── __init__.py
│   └── config.py           # Base URL, user credentials, timeouts
│
├── screenshots/            # Failure screenshots directory (auto-created)
├── reports/                # Pytest HTML report directory (auto-created)
│
├── conftest.py             # Pytest fixtures & failure screenshot hook
├── pytest.ini              # Pytest discovery & default options
├── requirements.txt        # Python package dependencies
├── README.md               # Framework documentation
└── .github/
    └── workflows/
        └── tests.yml       # GitHub Actions CI pipeline
```

---

## 🧪 Test Scenarios

The framework implements 10 comprehensive test cases covering positive, negative, and edge-case scenarios:

### 🔑 Login Tests (`tests/test_login.py`)
- `test_valid_login`: Logs in with `standard_user` and verifies redirection to the inventory catalog.
- `test_invalid_username`: Validates error message when providing an unregistered username.
- `test_invalid_password`: Validates error message when providing an incorrect password.
- `test_empty_credentials` *(Parametrized)*: Validates error messages when username, password, or both are omitted.
- `test_locked_out_user`: Verifies locked-out error message for `locked_out_user`.

### 🛒 Cart Tests (`tests/test_cart.py`)
- `test_add_single_product_to_cart`: Adds a single item, verifies cart badge count `1`, and verifies item title in cart page.
- `test_add_multiple_products_to_cart`: Adds 3 items, verifies badge count `3`, and validates all item names appear in cart.
- `test_remove_product_from_cart`: Adds items to cart, removes one item, and asserts it no longer appears in cart.

### ↕️ Sorting Tests (`tests/test_sorting.py`)
- `test_sort_products_price_low_to_high`: Sorts products by price ascending (`lohi`) and verifies price numerical order.
- `test_sort_products_name_z_to_a`: Sorts products by name descending (`za`) and verifies reverse alphabetical order.

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- **Google Chrome** browser installed.

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/your-username/qa-automation-framework.git
cd qa-automation-framework

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📊 Execution & Reports

### Run All Tests Locally
```bash
pytest
```

### Run Tests in Headed Mode (Browser Visible)
```bash
pytest --headless=false
```

### Run Tests in Microsoft Edge
```bash
pytest --browser=edge
```

### Generate Self-Contained HTML Test Report
```bash
pytest --html=reports/report.html --self-contained-html
```

After execution, open `reports/report.html` in any web browser to view detailed execution statistics, test pass/fail results, and attached screenshots on failure.

---

## 🤖 GitHub Actions CI/CD

The workflow specified in `.github/workflows/tests.yml` triggers automatically on every `push` and `pull_request` to the main branch.

**Pipeline Steps:**
1. Spins up an `ubuntu-latest` runner.
2. Installs Google Chrome in headless mode.
3. Installs Python dependencies from `requirements.txt`.
4. Executes the full Pytest automation suite.
5. Archives and publishes `reports/report.html` and failure screenshots as downloadable workflow artifacts.

---

## 🔮 Future Improvements

- **Cross-Browser Matrix**: Add Safari and Firefox matrix builds in GitHub Actions.
- **Data-Driven Testing**: Externalize test data into CSV or JSON files.
- **Allure Reporting**: Integrate Allure Framework for detailed step-by-step reporting dashboards.
- **API Test Layer**: Add API testing using `requests` module to validate backend endpoints alongside UI tests.
