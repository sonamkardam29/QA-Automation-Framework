"""
Product sorting automated test suite for SauceDemo.
"""

import time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import STANDARD_USER, PASSWORD


class TestSorting:

    def test_sort_products_price_low_to_high(self, driver):
        """Verify sorting products by Price (low to high) displays prices in ascending order."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        for attempt in range(2):
            try:
                inventory_page.sort_products("lohi")
                displayed_prices = inventory_page.get_product_prices()
                expected_prices = sorted(displayed_prices)
                assert displayed_prices == expected_prices, (
                    f"Prices are not sorted low to high! Actual: {displayed_prices}"
                )
                break
            except AssertionError as e:
                if attempt == 1:
                    raise e
                time.sleep(1)

    def test_sort_products_name_z_to_a(self, driver):
        """Verify sorting products by Name (Z to A) displays names in reverse alphabetical order."""
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        for attempt in range(2):
            try:
                inventory_page.sort_products("za")
                displayed_names = inventory_page.get_product_names()
                expected_names = sorted(displayed_names, reverse=True)
                assert displayed_names == expected_names, (
                    f"Names are not sorted Z to A! Actual: {displayed_names}"
                )
                break
            except AssertionError as e:
                if attempt == 1:
                    raise e
                time.sleep(1)
