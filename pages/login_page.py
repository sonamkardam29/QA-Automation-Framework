"""
LoginPage class representing the login screen of SauceDemo.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import BASE_URL, EXPLICIT_WAIT


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

        # Locators
        self._username_input = (By.ID, "user-name")
        self._password_input = (By.ID, "password")
        self._login_button = (By.ID, "login-button")
        self._error_message = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        """Navigate to the login page."""
        self.driver.get(BASE_URL)
        return self

    def enter_username(self, username):
        """Type username into input field."""
        element = self.wait.until(EC.element_to_be_clickable(self._username_input))
        element.clear()
        element.send_keys(username)
        return self

    def enter_password(self, password):
        """Type password into input field."""
        element = self.wait.until(EC.element_to_be_clickable(self._password_input))
        element.clear()
        element.send_keys(password)
        return self

    def click_login(self):
        """Click the login button."""
        element = self.wait.until(EC.element_to_be_clickable(self._login_button))
        element.click()
        return self

    def login(self, username, password):
        """Helper method to complete login flow in one step."""
        if username:
            self.enter_username(username)
        if password:
            self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        """Retrieve displayed error message text."""
        element = self.wait.until(EC.visibility_of_element_located(self._error_message))
        return element.text
