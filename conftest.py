"""
Pytest configuration, browser driver fixtures, and failure screenshot hooks.
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    """Add custom CLI options for pytest execution."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser choice: chrome or edge",
    )
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run browser in headless mode: true or false",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped Selenium WebDriver fixture.
    Initializes driver, configures timeouts and window size, and cleans up after test.
    """
    browser_name = request.config.getoption("--browser").lower()
    headless_opt = request.config.getoption("--headless").lower() == "true"

    driver_instance = None

    if browser_name == "edge":
        options = EdgeOptions()
        if headless_opt:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver_instance = webdriver.Edge(options=options)
    else:
        # Default to Chrome
        options = ChromeOptions()
        if headless_opt:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_instance = webdriver.Chrome(options=options)

    driver_instance.maximize_window()
    driver_instance.implicitly_wait(5)

    # Attach driver instance to request node for screenshot hook access
    request.node.driver = driver_instance

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure and embed in HTML report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_instance = getattr(item, "driver", None)
        if driver_instance:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("[", "_").replace("]", "_")
            filename = f"failure_{test_name}_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)

            try:
                driver_instance.save_screenshot(filepath)
                # Embed relative path into Pytest HTML report if available
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html is not None:
                    rel_path = os.path.join("..", "screenshots", filename)
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.image(filepath))
                    report.extra = extra
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
