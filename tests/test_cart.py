"""
Shopping cart functionality automated test suite for SauceDemo.
"""

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import STANDARD_USER, PASSWORD


class TestCart:

    def test_add_single_product_to_cart(self, driver):
        """Verify adding a single product displays item in cart and updates badge."""
        product_name = "Sauce Labs Backpack"

        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page.add_product_to_cart(product_name)
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge count should be 1."

        inventory_page.open_cart()
        assert cart_page.is_on_cart_page(), "User should be navigated to Cart page."

        cart_items = cart_page.get_cart_items()
        assert product_name in cart_items, (
            f"Expected '{product_name}' in cart items, found {cart_items}"
        )

    def test_add_multiple_products_to_cart(self, driver):
        """Verify adding multiple products updates cart badge and lists all items."""
        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ]

        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        for item in products_to_add:
            inventory_page.add_product_to_cart(item)

        badge_count = inventory_page.get_cart_badge_count()
        assert badge_count == len(products_to_add), (
            f"Expected badge count {len(products_to_add)}, but got {badge_count}"
        )

        inventory_page.open_cart()
        cart_items = cart_page.get_cart_items()

        for item in products_to_add:
            assert item in cart_items, f"Product '{item}' missing from cart list."

    def test_remove_product_from_cart(self, driver):
        """Verify removing a product from cart page updates item list."""
        product_to_add = "Sauce Labs Backpack"
        product_to_keep = "Sauce Labs Bike Light"

        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)

        login_page.open()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page.add_product_to_cart(product_to_add)
        inventory_page.add_product_to_cart(product_to_keep)

        inventory_page.open_cart()
        cart_page.remove_product(product_to_add)

        remaining_items = cart_page.get_cart_items()
        assert product_to_add not in remaining_items, (
            f"Product '{product_to_add}' should have been removed from cart."
        )
        assert product_to_keep in remaining_items, (
            f"Product '{product_to_keep}' should remain in cart."
        )
