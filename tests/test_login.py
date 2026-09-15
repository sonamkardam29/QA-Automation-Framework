"""
Login functionality automated test suite for SauceDemo.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import (
    STANDARD_USER,
    LOCKED_USER,
    INVALID_USER,
    PASSWORD,
    INVALID_PASSWORD,
)


class TestLogin:

    def test_valid_login(self, driver):
        """Verify successful login with valid credentials navigates to Inventory page."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        assert inventory_page.is_on_inventory_page(), (
            f"Expected user to land on Inventory page, but URL was '{driver.current_url}'"
        )

    def test_invalid_username(self, driver):
        """Verify login failure with invalid username displays expected error message."""
        login_page = LoginPage(driver)

        login_page.open()
        login_page.login(INVALID_USER, PASSWORD)

        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"Unexpected error message: '{error_text}'"
        )

    def test_invalid_password(self, driver):
        """Verify login failure with invalid password displays expected error message."""
        login_page = LoginPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, INVALID_PASSWORD)

        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"Unexpected error message: '{error_text}'"
        )

    @pytest.mark.parametrize(
        "username, password, expected_substring",
        [
            ("", PASSWORD, "Username is required"),
            (STANDARD_USER, "", "Password is required"),
            ("", "", "Username is required"),
        ],
        ids=["empty_user", "empty_pass", "empty_both"],
    )
    def test_empty_credentials(self, driver, username, password, expected_substring):
        """Parametrized test verifying validation errors for missing credentials."""
        login_page = LoginPage(driver)

        login_page.open()
        login_page.login(username, password)

        error_text = login_page.get_error_message()
        assert expected_substring in error_text, (
            f"Expected '{expected_substring}' in error, but got '{error_text}'"
        )

    def test_locked_out_user(self, driver):
        """Verify error message for locked-out user account."""
        login_page = LoginPage(driver)

        login_page.open()
        login_page.login(LOCKED_USER, PASSWORD)

        error_text = login_page.get_error_message()
        assert "Sorry, this user has been locked out." in error_text, (
            f"Unexpected error message for locked out user: '{error_text}'"
        )
